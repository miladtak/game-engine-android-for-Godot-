extends Control

@onready var scene_root: Node3D = $MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport/SceneRoot
@onready var camera: Camera3D = $MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport/SceneRoot/Camera3D
@onready var play_mode_btn: Button = $MainVBox/TopBar/PlayModeBtn
@onready var btn_export_apk: Button = $MainVBox/TopBar/BtnExportAPK

@onready var left_panel: PanelContainer = $MainVBox/MainSplit/LeftPanel
@onready var inspector_panel: PanelContainer = $MainVBox/MainSplit/RightSplit/InspectorPanel

@onready var btn_add_box: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddBox
@onready var btn_add_player: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddPlayer
@onready var btn_add_ground: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddGround
@onready var btn_save: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnSave
@onready var btn_load: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnLoad
@onready var asset_tree: Tree = $MainVBox/MainSplit/LeftPanel/VBox/AssetTree

@onready var input_pos_x: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputPosX
@onready var input_pos_y: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputPosY
@onready var input_pos_z: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputPosZ
@onready var input_scale_x: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputScaleX
@onready var input_scale_y: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputScaleY
@onready var input_scale_z: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputScaleZ
@onready var input_rot_y: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputRotY
@onready var btn_apply_props: Button = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/BtnApplyProps

var selected_node: Node3D = null
var is_dragging: bool = false

func _ready() -> void:
	if play_mode_btn: play_mode_btn.pressed.connect(_on_toggle_play_mode)
	if btn_export_apk: btn_export_apk.pressed.connect(_on_export_apk_clicked)
	if btn_add_box: btn_add_box.pressed.connect(_on_add_3d_box)
	if btn_add_player: btn_add_player.pressed.connect(_on_add_3d_player)
	if btn_add_ground: btn_add_ground.pressed.connect(_on_add_3d_ground)
	if btn_save: btn_save.pressed.connect(_on_save_project)
	if btn_load: btn_load.pressed.connect(_on_load_project)
	if btn_apply_props: btn_apply_props.pressed.connect(_on_apply_properties)
	
	mouse_filter = Control.MOUSE_FILTER_PASS

func _input(event: InputEvent) -> void:
	if Global.is_playing_preview:
		return
		
	if event is InputEventScreenTouch:
		if event.pressed:
			selected_node = null
			var closest_node = null
			var min_dist = 999999.0
			
			for child in scene_root.get_children():
				if child is Node3D and child.name != "Camera3D" and child.name != "DirectionalLight3D":
					if camera:
						var screen_pos = camera.unproject_position(child.global_position)
						var dist = screen_pos.distance_to(event.position)
						if dist < min_dist and dist < 140.0:
							min_dist = dist
							closest_node = child
							
			if closest_node:
				selected_node = closest_node
				is_dragging = true
				populate_inspector()
		else:
			is_dragging = false
			
	elif event is InputEventScreenDrag and is_dragging:
		if selected_node != null:
			selected_node.global_position.x += event.relative.x * 0.02
			selected_node.global_position.z += event.relative.y * 0.02
			populate_inspector()

func populate_inspector() -> void:
	if selected_node:
		if input_pos_x: input_pos_x.text = str(snapped(selected_node.global_position.x, 0.1))
		if input_pos_y: input_pos_y.text = str(snapped(selected_node.global_position.y, 0.1))
		if input_pos_z: input_pos_z.text = str(snapped(selected_node.global_position.z, 0.1))
		if input_scale_x: input_scale_x.text = str(snapped(selected_node.scale.x, 0.1))
		if input_scale_y: input_scale_y.text = str(snapped(selected_node.scale.y, 0.1))
		if input_scale_z: input_scale_z.text = str(snapped(selected_node.scale.z, 0.1))
		if input_rot_y: input_rot_y.text = str(snapped(selected_node.rotation_degrees.y, 0.1))

func _process(_delta: float) -> void:
	pass

func _on_add_3d_box() -> void:
	var body = RigidBody3D.new()
	body.name = "Box3D_" + str(randi() % 1000)
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
	body.position = Vector3(randf_range(-2, 2), 3, randf_range(-2, 2))
	scene_root.add_child(body)

func _on_add_3d_player() -> void:
	var player = CharacterBody3D.new()
	player.name = "Player3D_" + str(randi() % 1000)
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

func _on_add_3d_ground() -> void:
	var ground = StaticBody3D.new()
	ground.name = "Ground3D_" + str(randi() % 1000)
	var mesh_inst = MeshInstance3D.new()
	var plane = BoxMesh.new()
	plane.size = Vector3(6.0, 0.4, 6.0)
	mesh_inst.mesh = plane
	var col = CollisionShape3D.new()
	var shape = BoxShape3D.new()
	shape.size = Vector3(6.0, 0.4, 6.0)
	col.shape = shape
	ground.add_child(mesh_inst)
	ground.add_child(col)
	ground.position = Vector3(0, 0, 0)
	scene_root.add_child(ground)

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
		var px = input_pos_x.text.to_float()
		var py = input_pos_y.text.to_float()
		var pz = input_pos_z.text.to_float()
		selected_node.global_position = Vector3(px, py, pz)
		
		var sx = input_scale_x.text.to_float()
		var sy = input_scale_y.text.to_float()
		var sz = input_scale_z.text.to_float()
		selected_node.scale = Vector3(max(0.1, sx), max(0.1, sy), max(0.1, sz))
		
		var ry = input_rot_y.text.to_float()
		selected_node.rotation_degrees = Vector3(0, ry, 0)

func _on_save_project() -> void:
	var objects_data: Array = []
	for child in scene_root.get_children():
		if child is Node3D and child.name != "Camera3D" and child.name != "DirectionalLight3D":
			objects_data.append({
				"name": child.name,
				"pos_x": child.global_position.x,
				"pos_y": child.global_position.y,
				"pos_z": child.global_position.z,
				"scale_x": child.scale.x,
				"scale_y": child.scale.y,
				"scale_z": child.scale.z,
				"rot_y": child.rotation_degrees.y
			})
	Global.save_project(objects_data)

func _on_load_project() -> void:
	var loaded_objects = Global.load_project()
	for child in scene_root.get_children():
		if child.name != "Camera3D" and child.name != "DirectionalLight3D":
			child.queue_free()
	
	for obj_data in loaded_objects:
		var node = null
		if obj_data["name"].contains("Player3D"):
			_on_add_3d_player()
			node = scene_root.get_child(scene_root.get_child_count() - 1)
		elif obj_data["name"].contains("Ground3D"):
			_on_add_3d_ground()
			node = scene_root.get_child(scene_root.get_child_count() - 1)
		else:
			_on_add_3d_box()
			node = scene_root.get_child(scene_root.get_child_count() - 1)
			
		if node and node is Node3D:
			node.global_position = Vector3(obj_data.get("pos_x", 0), obj_data.get("pos_y", 0), obj_data.get("pos_z", 0))
			node.scale = Vector3(obj_data.get("scale_x", 1), obj_data.get("scale_y", 1), obj_data.get("scale_z", 1))
			node.rotation_degrees = Vector3(0, obj_data.get("rot_y", 0), 0)
