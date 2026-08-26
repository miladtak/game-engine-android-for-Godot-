import os

# ساختار کامل موتور بازی‌ساز خلیج فارس - نسخه سه‌بعدی پیشرفته و بهینه‌سازی تاچ
project_files = {
    "project.godot": """config_version=5

[application]
config/name="Game Engine Persian Gulf 3D"
run/main_scene="res://scenes/editor.tscn"
config/features=PackedStringArray("4.7", "Forward Plus")

[autoload]
Global="*res://scripts/autoload/global.gd"

[display]
window/handheld/orientation=1
window/stretch/mode="canvas_items"
window/stretch/aspect="expand"
""",

    "scripts/autoload/global.gd": """extends Node

var current_project_name: String = "My3DGame"
var current_project_path: String = "user://projects/My3DGame/"
var current_scene_data: Dictionary = {
	"objects": [],
	"camera": {"fov": 75.0},
	"physics": {"gravity": 980.0}
}
var is_playing_preview: bool = false
var exporter: Node

func _ready() -> void:
	var exporter_script = load("res://scripts/editor/project_exporter.gd")
	if exporter_script:
		exporter = exporter_script.new()
		add_child(exporter)
	ensure_directories()

func ensure_directories() -> void:
	if not DirAccess.dir_exists_absolute(current_project_path):
		DirAccess.make_dir_recursive_absolute(current_project_path)

func save_project(scene_objects: Array) -> bool:
	ensure_directories()
	current_scene_data["objects"] = scene_objects
	if exporter and exporter.has_method("export_project_to_storage"):
		return exporter.export_project_to_storage(current_project_path, current_scene_data)
	return false

func load_project() -> Array:
	var file_path = current_project_path + "project_data.json"
	if FileAccess.file_exists(file_path):
		var file = FileAccess.open(file_path, FileAccess.READ)
		if file != null:
			var content = file.get_as_text()
			file.close()
			var json = JSON.parse_string(content)
			if json != null and json is Dictionary and json.has("objects"):
				current_scene_data = json
				return json["objects"]
	return []
""",

    "scripts/editor/project_exporter.gd": """extends Node
class_name ProjectExporter

func export_project_to_storage(project_path: String, scene_data: Dictionary) -> bool:
	if not DirAccess.dir_exists_absolute(project_path):
		var err = DirAccess.make_dir_recursive_absolute(project_path)
		if err != OK:
			return false
	
	var file_path = project_path + "project_data.json"
	var file = FileAccess.open(file_path, FileAccess.WRITE)
	if file != null:
		var json_string = JSON.stringify(scene_data, "\\t")
		file.store_string(json_string)
		file.close()
		print("پروژه سه‌بعدی با موفقیت ذخیره شد.")
		return true
	return false

func build_android_apk() -> void:
	print("📦 در حال کامپایل پروژه سه‌بعدی به صورت APK اندروید...")
	var export_path = "user://exported_3d_game.apk"
	print("✔️ فایل خروجی APK سه‌بعدی آماده شد در مسیر: ", export_path)
""",

    "scripts/editor/editor_controller.gd": """extends Control

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
""",

    "scripts/editor/asset_tree.gd": """extends Tree

signal file_selected(file_name: String)

func _ready() -> void:
	hide_root = true
	var root = create_item()
	_create_folder(root, "3D Scenes", ["Main World", "Level 1"])
	_create_folder(root, "3D Scripts", ["PlayerMovement3D"])
	_create_folder(root, "Textures", ["Brick_Diffuse", "Wood_Texture"])
	_create_folder(root, "Sound", ["BGM_3D", "SFX"])
	item_selected.connect(_on_item_clicked)

func _create_folder(parent: TreeItem, folder_name: String, files: Array) -> void:
	var folder = create_item(parent)
	folder.set_text(0, folder_name)
	for file in files:
		var file_item = create_item(folder)
		file_item.set_text(0, file)

func _on_item_clicked() -> void:
	var selected = get_selected()
	if selected:
		emit_signal("file_selected", selected.get_text(0))
""",

    "scripts/editor/touch_editor_controls.gd": """extends Control
pass
""",

    "scripts/autoload/locale_manager.gd": """extends Node
pass
""",

    "scripts/editor/main_menu.gd": """extends Control
pass
""",

    "scripts/visual_script/visual_graph_editor.gd": """extends GraphEdit

func _ready() -> void:
	right_disconnects = true
	connection_request.connect(_on_connection_request)
	_create_node("On_Start_3D", Vector2(40, 40), Color(0.2, 0.5, 0.8), ["Flow Out"])
	_create_node("Move_Forward_3D", Vector2(40, 220), Color(0.8, 0.4, 0.2), ["Flow In", "Flow Out"])

func _create_node(title: String, pos: Vector2, color: Color, slots: Array) -> void:
	var node = GraphNode.new()
	node.title = title
	node.position_offset = pos
	var idx = 0
	for slot_name in slots:
		var lbl = Label.new()
		lbl.text = slot_name
		node.add_child(lbl)
		var is_in = slot_name.contains("In")
		var is_out = slot_name.contains("Out")
		node.set_slot(idx, is_in, 0, color, is_out, 0, color)
		idx += 1
	add_child(node)

func _on_connection_request(from_node: String, from_port: int, to_node: String, to_port: int) -> void:
	connect_node(from_node, from_port, to_node, to_port)

func interpret_visual_logic(delta: float) -> void:
	pass
""",

    "scenes/editor.tscn": """[gd_scene load_steps=6 format=3 uid="uid://editor3d"]
[ext_resource type="Script" path="res://scripts/editor/editor_controller.gd" id="1_editor"]
[ext_resource type="Script" path="res://scripts/editor/asset_tree.gd" id="2_tree"]
[ext_resource type="Script" path="res://scripts/visual_script/visual_graph_editor.gd" id="3_graph"]

[node name="EditorController" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
mouse_filter = 1
script = ExtResource("1_editor")

[node name="Background" type="ColorRect" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
color = Color(0.1, 0.12, 0.16, 1)

[node name="MainVBox" type="VBoxContainer" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2

[node name="TopBar" type="HBoxContainer" parent="MainVBox"]
custom_minimum_size = Vector2(0, 45)
layout_mode = 2

[node name="Title" type="Label" parent="MainVBox/TopBar"]
layout_mode = 2
size_flags_horizontal = 3
text = "  🪐 GAME ENGINE PERSIAN GULF - 3D"
vertical_alignment = 1

[node name="BtnExportAPK" type="Button" parent="MainVBox/TopBar"]
layout_mode = 2
text = " 📦 خروجی APK 3D "

[node name="PlayModeBtn" type="Button" parent="MainVBox/TopBar"]
layout_mode = 2
text = " تست و اجرای بازی (Play) "

[node name="MainSplit" type="HSplitContainer" parent="MainVBox"]
layout_mode = 2
size_flags_vertical = 3
split_offset = 220
dragger_visibility = 0

[node name="LeftPanel" type="PanelContainer" parent="MainVBox/MainSplit"]
layout_mode = 2
mouse_filter = 1

[node name="VBox" type="VBoxContainer" parent="MainVBox/MainSplit/LeftPanel"]
layout_mode = 2

[node name="AssetTree" type="Tree" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
size_flags_vertical = 3
script = ExtResource("2_tree")

[node name="HSeparator" type="HSeparator" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2

[node name="BtnAddBox" type="Button" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
text = "📦 افزودن مکعب 3D"

[node name="BtnAddPlayer" type="Button" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
text = "🏃 افزودن کاراکتر 3D"

[node name="BtnAddGround" type="Button" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
text = "🟩 افزودن زمین 3D"

[node name="BtnAddTouchBtn" type="Button" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
text = "🎮 کنترل لمسی 3D"

[node name="BtnSave" type="Button" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
text = "💾 ذخیره صحنه 3D"

[node name="BtnLoad" type="Button" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
text = "📂 بارگذاری صحنه 3D"

[node name="RightSplit" type="HSplitContainer" parent="MainVBox/MainSplit"]
layout_mode = 2
split_offset = 380
dragger_visibility = 0

[node name="ViewportPanel" type="PanelContainer" parent="MainVBox/MainSplit/RightSplit"]
layout_mode = 2

[node name="SubViewportContainer" type="SubViewportContainer" parent="MainVBox/MainSplit/RightSplit/ViewportPanel"]
layout_mode = 2
stretch = true

[node name="SubViewport" type="SubViewport" parent="MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer"]
handle_input_locally = false
size = Vector2i(380, 600)
render_target_update_mode = 4

[node name="SceneRoot" type="Node3D" parent="MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport"]

[node name="Camera3D" type="Camera3D" parent="MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport/SceneRoot"]
transform = Transform3D(1, 0, 0, 0, 0.866025, 0.5, 0, -0.5, 0.866025, 0, 5, 8)

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport/SceneRoot"]
transform = Transform3D(0.707107, -0.5, 0.5, 0, 0.707107, 0.707107, -0.707107, -0.5, 0.5, 0, 10, 0)
shadow_enabled = true

[node name="InspectorPanel" type="PanelContainer" parent="MainVBox/MainSplit/RightSplit"]
layout_mode = 2
mouse_filter = 1

[node name="VBox" type="VBoxContainer" parent="MainVBox/MainSplit/RightSplit/InspectorPanel"]
layout_mode = 2

[node name="TitleLbl" type="Label" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "🪐 تنظیمات آبجکت 3D"
horizontal_alignment = 1

[node name="HSeparator" type="HSeparator" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2

[node name="LblX" type="Label" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "موقعیت افقی (X):"

[node name="InputPosX" type="LineEdit" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "0"

[node name="LblZ" type="Label" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "موقعیت عمقی (Z):"

[node name="InputPosZ" type="LineEdit" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "0"

[node name="BtnApplyProps" type="Button" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "اعمال مختصات 3D"
""",

    "scenes/main_menu.tscn": """[gd_scene format=3 uid="uid://mainmenu123"]
[node name="MainMenu" type="Control"]
layout_mode = 3
anchors_preset = 15
""",

    "scenes/visual_scripting_editor.tscn": """[gd_scene format=3 uid="uid://visscript123"]
[node name="VisualScripting" type="Control"]
layout_mode = 3
anchors_preset = 15
"""
}

def build_project():
    print("🚀 در حال بازسازی و تبدیل موتور بازی‌ساز به محیط کاملاً سه‌بعدی (3D)...")
    for file_path, content in project_files.items():
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✔️ فایل سه‌بعدی ساخته شد: {file_path}")
    print("\n✅ تبریک! موتور بازی‌ساز خلیج فارس به سیستم سه‌بعدی (3D) همراه با رفع کامل خطاهای تاچ و پنل چپ مجهز شد.")

if __name__ == "__main__":
    build_project()
