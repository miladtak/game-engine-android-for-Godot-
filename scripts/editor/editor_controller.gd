extends Control

@onready var scene_root: Node3D = $MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport/SceneRoot
@onready var play_mode_btn: Button = $MainVBox/TopBar/PlayModeBtn
@onready var btn_export_apk: Button = $MainVBox/TopBar/BtnExportAPK

@onready var left_panel: PanelContainer = $MainVBox/MainSplit/LeftPanel
@onready var inspector_panel: PanelContainer = $MainVBox/MainSplit/RightSplit/InspectorPanel

@onready var btn_add_box: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddBox
@onready var btn_add_player: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddPlayer
@onready var btn_add_ground: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddGround
@onready var btn_add_touch_btn: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddTouchBtn
@onready var btn_save: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnSave
@onready var btn_load: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnLoad
@onready var asset_tree: Tree = $MainVBox/MainSplit/LeftPanel/VBox/AssetTree

@onready var input_pos_x: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputPosX
@onready var input_pos_z: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputPosZ
@onready var btn_apply_props: Button = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/BtnApplyProps

var selected_node: Node3D = null
var is_dragging: bool = false

func _ready() -> void:
	if play_mode_btn: play_mode_btn.pressed.connect(_on_toggle_play_mode)
	if btn_export_apk: btn_export_apk.pressed.connect(_on_export_apk_clicked)
	if btn_add_box: btn_add_box.pressed.connect(_on_add_3d_box)
	if btn_add_player: btn_add_player.pressed.connect(_on_add_3d_player)
	if btn_add_ground: btn_add_ground.pressed.connect(_on_add_3d_ground)
	if btn_add_touch_btn: btn_add_touch_btn.pressed.connect(_on_add_touch_button)
	if btn_save: btn_save.pressed.connect(_on_save_project)
	if btn_load: btn_load.pressed.connect(_on_load_project)
	if btn_apply_props: btn_apply_props.pressed.connect(_on_apply_properties)
	
	# اطمینان از عملکرد صحیح تاچ و موس روی پنل‌ها
	mouse_filter = Control.MOUSE_FILTER_PASS

func _input(event: InputEvent) -> void:
	if Global.is_playing_preview:
		return
		
	# سیستم جابه‌جایی سه‌بعدی اشیاء با لمس صفحه در ویوپورت
	if event is InputEventScreenTouch:
		if event.pressed:
			selected_node = null
			for child in scene_root.get_children():
				if child is Node3D and child.name != "Camera3D" and child.name != "DirectionalLight3D":
					# ساده‌سازی انتخاب بر اساس فاصله دوبرابری تپ روی صفحه
					selected_node = child
					is_dragging = true
					if input_pos_x and input_pos_y_exists():
						input_pos_x.text = str(snapped(child.global_position.x, 0.1))
						if input_pos_z: input_pos_z.text = str(snapped(child.global_position.z, 0.1))
					break
		else:
			is_dragging = false
			
	elif event is InputEventScreenDrag and is_dragging:
		if selected_node != null:
			# حرکت سه‌بعدی روی صفحه افقی X و Z بر اساس درگ انگشت
			selected_node.global_position.x += event.relative.x * 0.02
			selected_node.global_position.z += event.relative.y * 0.02
			if input_pos_x: input_pos_x.text = str(snapped(selected_node.global_position.x, 0.1))
			if input_pos_z: input_pos_z.text = str(snapped(selected_node.global_position.z, 0.1))

func input_pos_y_exists() -> bool:
	return true

func _process(delta: float) -> void:
	if Global.is_playing_preview:
		var graph_editor = get_node_or_null("../MainVBox/MainSplit/RightSplit/GraphPanel/VisualGraphEditor")
		if graph_editor and graph_editor.has_method("interpret_visual_logic"):
			graph_editor.interpret_visual_logic(delta)

# افزودن مکعب سه‌بعدی (3D Box / RigidBody3D)
func _on_add_3d_box() -> void:
	var body = RigidBody3D.new()
	body.name = "Box3D"
	
	var mesh_inst = MeshInstance3D.new()
	var box_mesh = BoxMesh.new()
	box_mesh.size = Vector3(1.5, 1.5, 1.5)
	mesh_inst.mesh = box_mesh
	
	var col = CollisionShape3D.new()
	var shape = BoxShape3D.new()
	shape.size = Vector3(1.5, 1.5, 1.5)
	col.shape = shape
	
	body.add_child(mesh_inst)
	body.add_child(col)
	body.position = Vector3(0, 3, 0)
	scene_root.add_child(body)
	print("📦 آبجکت مکعب سه‌بعدی اضافه شد.")

# افزودن کاراکتر سه‌بعدی (CharacterBody3D)
func _on_add_3d_player() -> void:
	var player = CharacterBody3D.new()
	player.name = "Player3D"
	
	var mesh_inst = MeshInstance3D.new()
	var capsule = CapsuleMesh.new()
	capsule.radius = 0.5
	capsule.height = 2.0
	mesh_inst.mesh = capsule
	
	var col = CollisionShape3D.new()
	var shape = CapsuleShape3D.new()
	shape.radius = 0.5
	shape.height = 2.0
	col.shape = shape
	
	player.add_child(mesh_inst)
	player.add_child(col)
	player.position = Vector3(0, 2, 0)
	scene_root.add_child(player)
	print("🏃 کاراکتر سه‌بعدی اضافه شد.")

# افزودن زمین سه‌بعدی (StaticBody3D)
func _on_add_3d_ground() -> void:
	var ground = StaticBody3D.new()
	ground.name = "Ground3D"
	
	var mesh_inst = MeshInstance3D.new()
	var plane = BoxMesh.new()
	plane.size = Vector3(10.0, 0.5, 10.0)
	mesh_inst.mesh = plane
	
	var col = CollisionShape3D.new()
	var shape = BoxShape3D.new()
	shape.size = Vector3(10.0, 0.5, 10.0)
	col.shape = shape
	
	ground.add_child(mesh_inst)
	ground.add_child(col)
	ground.position = Vector3(0, -0.5, 0)
	scene_root.add_child(ground)
	print("🟩 زمین سه‌بعدی اضافه شد.")

func _on_add_touch_button() -> void:
	var touch_panel = Panel.new()
	touch_panel.name = "TouchControl3D"
	touch_panel.size = Vector2(80, 80)
	touch_panel.position = Vector2(100, 350)
	var btn = Button.new()
	btn.text = "⬆️ پرش 3D"
	btn.size = Vector2(80, 80)
	touch_panel.add_child(btn)
	scene_root.get_parent().add_child(touch_panel)

func _on_toggle_play_mode() -> void:
	Global.is_playing_preview = not Global.is_playing_preview
	if Global.is_playing_preview:
		play_mode_btn.text = " توقف بازی (Stop) "
		play_mode_btn.modulate = Color(1, 0.4, 0.4)
		if left_panel: left_panel.visible = false
		if inspector_panel: inspector_panel.visible = false
	else:
		play_mode_btn.text = " تست و اجرای بازی (Play) "
		play_mode_btn.modulate = Color(1, 1, 1)
		if left_panel: left_panel.visible = true
		if inspector_panel: inspector_panel.visible = true
		
	for child in scene_root.get_children():
		if child is RigidBody3D:
			child.freeze = not Global.is_playing_preview

func _on_export_apk_clicked() -> void:
	if Global.exporter and Global.exporter.has_method("build_android_apk"):
		Global.exporter.build_android_apk()

func _on_apply_properties() -> void:
	if selected_node != null and selected_node is Node3D:
		var nx = input_pos_x.text.to_float()
		var nz = input_pos_z.text.to_float()
		selected_node.global_position = Vector3(nx, selected_node.global_position.y, nz)
		print("مختصات سه‌بعدی اعمال شد.")

func _on_save_project() -> void:
	var objects_data: Array = []
	for child in scene_root.get_children():
		if child is Node3D and child.name != "Camera3D" and child.name != "DirectionalLight3D":
			objects_data.append({
				"name": child.name,
				"pos_x": child.global_position.x,
				"pos_y": child.global_position.y,
				"pos_z": child.global_position.z
			})
	if Global.save_project(objects_data):
		print("پروژه سه‌بعدی ذخیره شد!")

func _on_load_project() -> void:
	var loaded_objects = Global.load_project()
	for child in scene_root.get_children():
		if child.name != "Camera3D" and child.name != "DirectionalLight3D":
			child.queue_free()
	
	for obj_data in loaded_objects:
		if obj_data["name"].contains("Player3D"):
			_on_add_3d_player()
		elif obj_data["name"].contains("Ground3D"):
			_on_add_3d_ground()
		else:
			_on_add_3d_box()
	print("پروژه سه‌بعدی بارگذاری شد!")
