import os

# ساختار کامل فایل‌ها و کدهای موتور بازی‌ساز
project_files = {
    "project.godot": """config_version=5

[application]
config/name="Game Engine Persian Gulf"
run/main_scene="res://scenes/main_menu.tscn"
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
	# Load ProjectExporter dynamically to avoid cyclic parsing issues
	var exporter_script = load("res://scripts/editor/project_exporter.gd")
	if exporter_script:
		exporter = exporter_script.new()
		add_child(exporter)
	ensure_directories()

func ensure_directories() -> void:
	if not DirAccess.dir_exists_absolute(current_project_path):
		DirAccess.make_dir_recursive_absolute(current_project_path)

func save_project() -> bool:
	ensure_directories()
	if exporter and exporter.has_method("export_project_to_storage"):
		return exporter.export_project_to_storage(current_project_path, current_scene_data)
	return false

func load_project(proj_name: String) -> bool:
	current_project_name = proj_name
	current_project_path = "user://projects/" + proj_name + "/"
	var file_path = current_project_path + "project_data.json"
	
	if FileAccess.file_exists(file_path):
		var file = FileAccess.open(file_path, FileAccess.READ)
		if file != null:
			var content = file.get_as_text()
			file.close()
			var json = JSON.parse_string(content)
			if json != null and json is Dictionary:
				current_scene_data = json
				return true
	return false
""",

    "scripts/editor/project_exporter.gd": """extends Node
class_name ProjectExporter

# ذخیره‌سازی داده‌های صحنه روی پوشه مشخص شده در حافظه دستگاه
func export_project_to_storage(project_path: String, scene_data: Dictionary) -> bool:
	if not DirAccess.dir_exists_absolute(project_path):
		var err = DirAccess.make_dir_recursive_absolute(project_path)
		if err != OK:
			print("خطا در ایجاد پوشه پروژه: ", err)
			return false
	
	var file_path = project_path + "project_data.json"
	var file = FileAccess.open(file_path, FileAccess.WRITE)
	if file != null:
		var json_string = JSON.stringify(scene_data, "\\t")
		file.store_string(json_string)
		file.close()
		print("پروژه با موفقیت ذخیره شد: ", file_path)
		return true
	else:
		print("خطا در باز کردن فایل ذخیره! کد خطا: ", FileAccess.get_open_error())
		return false
""",

    "scripts/editor/editor_controller.gd": """extends Control

@onready var scene_root: Node2D = $MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport/SceneRoot
@onready var play_mode_btn: Button = $MainVBox/TopBar/PlayModeBtn

func _ready() -> void:
	if play_mode_btn:
		play_mode_btn.pressed.connect(_on_toggle_play_mode)

func _on_toggle_play_mode() -> void:
	Global.is_playing_preview = not Global.is_playing_preview
	
	if Global.is_playing_preview:
		play_mode_btn.text = " توقف بازی "
		play_mode_btn.modulate = Color(1, 0.4, 0.4) # رنگ قرمز
	else:
		play_mode_btn.text = " حالت بازی "
		play_mode_btn.modulate = Color(1, 1, 1) # رنگ پیش‌فرض
		
	# اعمال فیزیک به اشیاء داخل صحنه
	for child in scene_root.get_children():
		if child is RigidBody2D:
			child.freeze = not Global.is_playing_preview
""",

    "scripts/editor/asset_tree.gd": """extends Tree

func _ready() -> void:
	# پیکربندی ظاهر درختی
	hide_root = true
	var root = create_item()
	
	# ساخت ساختار پوشه‌های موتور
	_create_folder(root, "Scenes", ["Main Level", "Start Screen"])
	_create_folder(root, "Scripts", ["PlayerControl", "AIBehavior"])
	_create_folder(root, "Textures", ["CharacterSprites", "Environment"])
	_create_folder(root, "Sound", ["BGM", "SFX"])
	_create_folder(root, "Plugins", ["AI_Behavior_Pack", "Cutscene_Creator"])
	_create_folder(root, "Items", ["Item_Bag", "Item_Type"])

func _create_folder(parent: TreeItem, folder_name: String, files: Array) -> void:
	var folder = create_item(parent)
	folder.set_text(0, folder_name)
	
	for file in files:
		var file_item = create_item(folder)
		file_item.set_text(0, file)
""",

    "scripts/editor/touch_editor_controls.gd": """extends Control
# فایل پشتیبان برای کنترل‌های لمسی پیشرفته در آینده
pass
""",

    "scripts/autoload/locale_manager.gd": """extends Node
# مدیریت زبان‌ها (فارسی / انگلیسی)
pass
""",

    "scripts/editor/main_menu.gd": """extends Control
# اسکریپت منوی اصلی
pass
""",

    "scripts/visual_script/visual_graph_editor.gd": """extends GraphEdit

func _ready() -> void:
	# تنظیمات گراف
	right_disconnects = true
	connection_request.connect(_on_connection_request)
	
	# ساخت چند بلوک تستی شبیه عکس
	_create_node("On_Start", Vector2(40, 40), Color(0.2, 0.5, 0.8), ["Flow Out"])
	_create_node("Variable: Player_Object", Vector2(80, 120), Color(0.3, 0.4, 0.7), ["Flow In", "Flow Out"])
	_create_node("Get_Item", Vector2(40, 300), Color(0.4, 0.5, 0.9), ["Flow In", "تعداد آیتم Out"])

func _create_node(title: String, pos: Vector2, color: Color, slots: Array) -> void:
	var node = GraphNode.new()
	node.title = title
	node.position_offset = pos
	
	# ساخت پورت‌های ورودی و خروجی برای سیم‌کشی
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
custom_minimum_size = Vector2(0, 50)
layout_mode = 2

[node name="Title" type="Label" parent="MainVBox/TopBar"]
layout_mode = 2
size_flags_horizontal = 3
theme_override_font_sizes/font_size = 20
text = "  ⚙️ GAME ENGINE PERSIAN GULF"
vertical_alignment = 1

[node name="Tabs" type="HBoxContainer" parent="MainVBox/TopBar"]
layout_mode = 2
alignment = 1

[node name="BtnBuild" type="Button" parent="MainVBox/TopBar/Tabs"]
layout_mode = 2
text = "Build"
flat = true

[node name="BtnAssets" type="Button" parent="MainVBox/TopBar/Tabs"]
layout_mode = 2
text = "Assets"
flat = true

[node name="BtnSettings" type="Button" parent="MainVBox/TopBar/Tabs"]
layout_mode = 2
text = "Settings"
flat = true

[node name="PlayModeBtn" type="Button" parent="MainVBox/TopBar"]
layout_mode = 2
text = " حالت بازی "

[node name="MainSplit" type="HSplitContainer" parent="MainVBox"]
layout_mode = 2
size_flags_vertical = 3
split_offset = 250

[node name="LeftPanel" type="PanelContainer" parent="MainVBox/MainSplit"]
layout_mode = 2

[node name="AssetTree" type="Tree" parent="MainVBox/MainSplit/LeftPanel"]
layout_mode = 2
script = ExtResource("2_tree")

[node name="RightSplit" type="HSplitContainer" parent="MainVBox/MainSplit"]
layout_mode = 2
split_offset = 500

[node name="ViewportPanel" type="PanelContainer" parent="MainVBox/MainSplit/RightSplit"]
layout_mode = 2

[node name="SubViewportContainer" type="SubViewportContainer" parent="MainVBox/MainSplit/RightSplit/ViewportPanel"]
layout_mode = 2
stretch = true

[node name="SubViewport" type="SubViewport" parent="MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer"]
handle_input_locally = false
size = Vector2i(500, 500)
render_target_update_mode = 4

[node name="SceneRoot" type="Node2D" parent="MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport"]

[node name="GraphPanel" type="PanelContainer" parent="MainVBox/MainSplit/RightSplit"]
layout_mode = 2

[node name="VisualGraphEditor" type="GraphEdit" parent="MainVBox/MainSplit/RightSplit/GraphPanel"]
layout_mode = 2
script = ExtResource("3_graph")
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
    print("🚀 در حال ساخت ساختار موتور بازی‌ساز (Game Engine Persian Gulf)...")
    for file_path, content in project_files.items():
        # جدا کردن نام پوشه از مسیر فایل
        directory = os.path.dirname(file_path)
        
        # اگر فایل داخل پوشه است، ابتدا پوشه را بساز
        if directory:
            os.makedirs(directory, exist_ok=True)
            
        # نوشتن محتوا داخل فایل
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"✔️ فایل ایجاد شد: {file_path}")
        
    print("\n✅ پروژه با موفقیت ایجاد شد! حالا می‌توانید آن را در گودوت باز کنید.")

if __name__ == "__main__":
    build_project()
