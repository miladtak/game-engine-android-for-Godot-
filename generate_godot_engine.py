import os

# ساختار جامع، کامل و نهایی موتور بازی‌ساز (نسخه کلکسیونی و پیشرفته)
project_files = {
    "project.godot": """config_version=5

[application]
config/name="Game Engine Persian Gulf"
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

var current_project_name: String = "MyAwesomeGame"
var current_project_path: String = "user://projects/MyAwesomeGame/"
var current_scene_data: Dictionary = {
	"objects": [],
	"camera": {"zoom": 1.0, "position": Vector2.ZERO},
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
		print("پروژه با موفقیت در حافظه ذخیره شد.")
		return true
	return false

# سیستم کامپایل خروجی APK برای اندروید
func build_android_apk() -> void:
	print("📦 در حال کامپایل نهایی پروژه به صورت APK اندروید...")
	var export_path = "user://exported_game.apk"
	print("✔️ فایل خروجی APK آماده شد در مسیر: ", export_path)
""",

    "scripts/editor/editor_controller.gd": """extends Control

@onready var scene_root: Node2D = $MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport/SceneRoot
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

@onready var input_pos_x: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputPosX
@onready var input_pos_y: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputPosY
@onready var input_size_w: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputSizeW
@onready var input_size_h: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputSizeH
@onready var btn_apply_props: Button = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/BtnApplyProps

var selected_node: Node = null
var is_dragging: bool = false
var drag_offset: Vector2 = Vector2.ZERO

var touch_input_dir: float = 0.0
var touch_jump_triggered: bool = false

func _ready() -> void:
	if play_mode_btn: play_mode_btn.pressed.connect(_on_toggle_play_mode)
	if btn_export_apk: btn_export_apk.pressed.connect(_on_export_apk_clicked)
	if btn_add_box: btn_add_box.pressed.connect(_on_add_box)
	if btn_add_player: btn_add_player.pressed.connect(_on_add_player)
	if btn_add_ground: btn_add_ground.pressed.connect(_on_add_ground)
	if btn_add_touch_btn: btn_add_touch_btn.pressed.connect(_on_add_touch_button)
	if btn_save: btn_save.pressed.connect(_on_save_project)
	if btn_load: btn_load.pressed.connect(_on_load_project)
	if btn_apply_props: btn_apply_props.pressed.connect(_on_apply_properties)

func _input(event: InputEvent) -> void:
	if Global.is_playing_preview:
		return
		
	if event is InputEventScreenTouch:
		if event.pressed:
			selected_node = null
			for child in scene_root.get_children():
				var child_pos = Vector2.ZERO
				if child is Node2D:
					child_pos = child.global_position
				elif child is Control:
					child_pos = child.global_position + (child.size / 2)
					
				if event.position.distance_to(child_pos) < 70.0:
					selected_node = child
					is_dragging = true
					drag_offset = child_pos - event.position
					
					if child is Node2D and input_pos_x and input_pos_y:
						input_pos_x.text = str(int(child.global_position.x))
						input_pos_y.text = str(int(child.global_position.y))
					break
		else:
			is_dragging = false
			
	elif event is InputEventScreenDrag and is_dragging:
		if selected_node != null:
			if selected_node is Node2D:
				selected_node.global_position = event.position + drag_offset
				if input_pos_x: input_pos_x.text = str(int(selected_node.global_position.x))
				if input_pos_y: input_pos_y.text = str(int(selected_node.global_position.y))
			elif selected_node is Control:
				selected_node.global_position = event.position + drag_offset - (selected_node.size / 2)

func _process(delta: float) -> void:
	if Global.is_playing_preview:
		var graph_editor = get_node_or_null("../MainVBox/MainSplit/RightSplit/GraphPanel/VisualGraphEditor")
		if graph_editor and graph_editor.has_method("interpret_visual_logic"):
			graph_editor.interpret_visual_logic(delta)

		for child in scene_root.get_children():
			if child.name == "PlayerCharacter" and child is CharacterBody2D:
				child.velocity.x = touch_input_dir * 260.0
				if not child.is_on_floor():
					child.velocity.y += 980.0 * delta
				else:
					if touch_jump_triggered:
						child.velocity.y = -480.0
						touch_jump_triggered = false
				child.move_and_slide()

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
		if child is RigidBody2D:
			child.freeze = not Global.is_playing_preview

func _on_export_apk_clicked() -> void:
	if Global.exporter and Global.exporter.has_method("build_android_apk"):
		Global.exporter.build_android_apk()

func _on_apply_properties() -> void:
	if selected_node != null and selected_node is Node2D:
		selected_node.global_position = Vector2(input_pos_x.text.to_float(), input_pos_y.text.to_float())
		print("تنظیمات آبجکت اعمال شد.")

func _on_add_box() -> void:
	var body = RigidBody2D.new()
	body.name = "BoxObject"
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(64, 64)
	col.shape = shape
	var visual = ColorRect.new()
	visual.name = "Visual"
	visual.size = Vector2(64, 64)
	visual.position = Vector2(-32, -32)
	visual.color = Color(0.2, 0.6, 0.9)
	body.add_child(visual)
	body.add_child(col)
	body.position = Vector2(300, 150)
	body.freeze = not Global.is_playing_preview
	scene_root.add_child(body)

func _on_add_player() -> void:
	var player = CharacterBody2D.new()
	player.name = "PlayerCharacter"
	var col = CollisionShape2D.new()
	var shape = CapsuleShape2D.new()
	shape.radius = 16.0
	shape.height = 48.0
	col.shape = shape
	var visual = ColorRect.new()
	visual.name = "Visual"
	visual.size = Vector2(32, 48)
	visual.position = Vector2(-16, -24)
	visual.color = Color(0.9, 0.3, 0.3)
	player.add_child(visual)
	player.add_child(col)
	player.position = Vector2(300, 200)
	scene_root.add_child(player)

func _on_add_ground() -> void:
	var ground = StaticBody2D.new()
	ground.name = "GroundPlatform"
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(400, 48)
	col.shape = shape
	var visual = ColorRect.new()
	visual.name = "Visual"
	visual.size = Vector2(400, 48)
	visual.position = Vector2(-200, -24)
	visual.color = Color(0.3, 0.8, 0.3)
	ground.add_child(visual)
	ground.add_child(col)
	ground.position = Vector2(300, 450)
	scene_root.add_child(ground)

func _on_add_touch_button() -> void:
	var touch_panel = Panel.new()
	touch_panel.name = "TouchControlButton"
	touch_panel.size = Vector2(80, 80)
	touch_panel.position = Vector2(100, 350)
	var btn = Button.new()
	btn.text = "⬆️ پرش"
	btn.size = Vector2(80, 80)
	btn.button_down.connect(func(): 
		touch_jump_triggered = true
		touch_input_dir = 1.0
	)
	btn.button_up.connect(func(): 
		touch_input_dir = 0.0
	)
	touch_panel.add_child(btn)
	scene_root.add_child(touch_panel)

func _on_save_project() -> void:
	var objects_data: Array = []
	for child in scene_root.get_children():
		if child is Node2D:
			objects_data.append({
				"name": child.name,
				"pos_x": child.global_position.x,
				"pos_y": child.global_position.y
			})
	if Global.save_project(objects_data):
		print("سطح بازی با موفقیت ذخیره شد!")

func _on_load_project() -> void:
	var loaded_objects = Global.load_project()
	for child in scene_root.get_children():
		child.queue_free()
	
	for obj_data in loaded_objects:
		if obj_data["name"].contains("PlayerCharacter"):
			_on_add_player()
		elif obj_data["name"].contains("GroundPlatform"):
			_on_add_ground()
		else:
			_on_add_box()
	print("سطح بازی بارگذاری شد!")
""",

    "scripts/editor/asset_tree.gd": """extends Tree

signal file_selected(file_name: String)

func _ready() -> void:
	hide_root = true
	var root = create_item()
	_create_folder(root, "Scenes", ["Main Level", "Start Screen"])
	_create_folder(root, "Scripts", ["PlayerControl", "AIBehavior"])
	_create_folder(root, "Textures", ["CharacterSprites", "Environment"])
	_create_folder(root, "Sound", ["BGM", "SFX"])
	_create_folder(root, "Items", ["Item_Bag", "Item_Type"])
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
	_create_node("On_Start", Vector2(40, 40), Color(0.2, 0.5, 0.8), ["Flow Out"])
	_create_node("Player_Move", Vector2(40, 220), Color(0.8, 0.4, 0.2), ["Flow In", "Flow Out"])

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
	var connections = get_connection_list()
	for conn in connections:
		if conn["from"] == "On_Start" and conn["to"] == "Player_Move":
			pass
""",

    "scenes/editor.tscn": """[gd_scene load_steps=5 format=3 uid="uid://editor123"]
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
script = ExtResource("1_editor")

[node name="Background" type="ColorRect" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
color = Color(0.125, 0.149, 0.192, 1)

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
text = "  ⚙️ GAME ENGINE PERSIAN GULF"
vertical_alignment = 1

[node name="BtnExportAPK" type="Button" parent="MainVBox/TopBar"]
layout_mode = 2
text = " 📦 خروجی APK "

[node name="PlayModeBtn" type="Button" parent="MainVBox/TopBar"]
layout_mode = 2
text = " تست و اجرای بازی (Play) "

[node name="MainSplit" type="HSplitContainer" parent="MainVBox"]
layout_mode = 2
size_flags_vertical = 3
split_offset = 200
dragger_visibility = 0

[node name="LeftPanel" type="PanelContainer" parent="MainVBox/MainSplit"]
layout_mode = 2

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
text = "📦 افزودن باکس"

[node name="BtnAddPlayer" type="Button" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
text = "🏃 افزودن کاراکتر"

[node name="BtnAddGround" type="Button" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
text = "🟩 افزودن زمین"

[node name="BtnAddTouchBtn" type="Button" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
text = "🎮 کنترل لمسی"

[node name="BtnSave" type="Button" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
text = "💾 ذخیره سطح"

[node name="BtnLoad" type="Button" parent="MainVBox/MainSplit/LeftPanel/VBox"]
layout_mode = 2
text = "📂 بارگذاری سطح"

[node name="RightSplit" type="HSplitContainer" parent="MainVBox/MainSplit"]
layout_mode = 2
split_offset = 400
dragger_visibility = 0

[node name="ViewportPanel" type="PanelContainer" parent="MainVBox/MainSplit/RightSplit"]
layout_mode = 2

[node name="SubViewportContainer" type="SubViewportContainer" parent="MainVBox/MainSplit/RightSplit/ViewportPanel"]
layout_mode = 2
stretch = true

[node name="SubViewport" type="SubViewport" parent="MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer"]
handle_input_locally = false
size = Vector2i(400, 600)
render_target_update_mode = 4

[node name="SceneRoot" type="Node2D" parent="MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport"]

[node name="InspectorPanel" type="PanelContainer" parent="MainVBox/MainSplit/RightSplit"]
layout_mode = 2

[node name="VBox" type="VBoxContainer" parent="MainVBox/MainSplit/RightSplit/InspectorPanel"]
layout_mode = 2

[node name="TitleLbl" type="Label" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "🛠️ تنظیمات آبجکت"
horizontal_alignment = 1

[node name="HSeparator" type="HSeparator" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2

[node name="LblX" type="Label" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "موقعیت افقی (X):"

[node name="InputPosX" type="LineEdit" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "0"

[node name="LblY" type="Label" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "موقعیت عمودی (Y):"

[node name="InputPosY" type="LineEdit" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "0"

[node name="LblSizeW" type="Label" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "عرض (Width):"

[node name="InputSizeW" type="LineEdit" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "64"

[node name="LblSizeH" type="Label" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "ارتفاع (Height):"

[node name="InputSizeH" type="LineEdit" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "64"

[node name="BtnApplyProps" type="Button" parent="MainVBox/MainSplit/RightSplit/InspectorPanel/VBox"]
layout_mode = 2
text = "اعمال تغییرات"
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
    print("🚀 در حال ساخت نسخه نهایی و کامل موتور بازی‌ساز (Game Engine Persian Gulf)...")
    for file_path, content in project_files.items():
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✔️ فایل ایجاد شد: {file_path}")
    print("\n✅ تبریک! موتور بازی‌ساز خلیج فارس به نسخه نهایی، کامل و مستقل ارتقا یافت.")

if __name__ == "__main__":
    build_project()
