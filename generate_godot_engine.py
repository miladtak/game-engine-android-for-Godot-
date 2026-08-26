import os

files_to_create = {
    # 1. تنظیمات اصلی پروژه گودوت ۴
    "project.godot": """config_version=5

[application]
config/name="Game Engine Persian Gulf"
config/description="Advanced 2D/3D Mobile Game Development Engine built with Godot"
run/main_scene="res://scenes/main_menu.tscn"
config/features=PackedStringArray("4.3", "Forward Plus")
config/icon="res://icon.svg"

[autoload]
Global="*res://scripts/autoload/global.gd"
LocaleManager="*res://scripts/autoload/locale_manager.gd"

[display]
window/size/viewport_width=1280
window/size/viewport_height=720
window/stretch/mode="canvas_items"
window/stretch/aspect="expand"
window/handheld/orientation=0

[internationalization]
locale/translations=PackedStringArray("res://i18n/translations.fa.translation", "res://i18n/translations.en.translation")
locale/fallback="fa"
""",

    # 2. اسکریپت سراسری Global.gd
    "scripts/autoload/global.gd": """extends Node

var current_project_name: String = "MyAwesomeGame"
var current_project_path: String = "user://projects/MyAwesomeGame/"
var current_scene_data: Dictionary = {
    "objects": [],
    "camera": {"zoom": 1.0, "position": Vector2.ZERO},
    "physics": {"gravity": 980.0}
}
var is_playing_preview: bool = false

func _ready() -> void:
    ensure_directories()

func ensure_directories() -> void:
    DirAccess.make_dir_recursive_absolute("user://projects/")

func save_project() -> bool:
    var file = FileAccess.open(current_project_path + "project_data.json", FileAccess.WRITE)
    if file:
        file.store_string(JSON.stringify(current_scene_data, "\\t"))
        file.close()
        return true
    return false

func load_project(proj_name: String) -> bool:
    current_project_name = proj_name
    current_project_path = "user://projects/" + proj_name + "/"
    var file_path = current_project_path + "project_data.json"
    if FileAccess.file_exists(file_path):
        var file = FileAccess.open(file_path, FileAccess.READ)
        var content = file.get_as_text()
        file.close()
        var json = JSON.parse_string(content)
        if json:
            current_scene_data = json
            return true
    return false
""",

    # 3. سیستم چندزبانه و RTL
    "scripts/autoload/locale_manager.gd": """extends Node

var current_locale: String = "fa"

func _ready() -> void:
    set_language("fa")

func set_language(lang_code: String) -> void:
    current_locale = lang_code
    TranslationServer.set_locale(lang_code)

func is_rtl() -> bool:
    return current_locale == "fa" or current_locale == "ar"
""",

    # 4. منوی اصلی (Main Menu)
    "scenes/main_menu.tscn": """[gd_scene load_steps=2 format=3 uid="uid://mainmenu001"]

[ext_resource type="Script" path="res://scripts/editor/main_menu.gd" id="1_menu"]

[node name="MainMenu" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1_menu")

[node name="Background" type="ColorRect" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
color = Color(0.117647, 0.12549, 0.160784, 1)

[node name="HeaderLabel" type="Label" parent="."]
layout_mode = 1
anchors_preset = 5
anchor_left = 0.5
anchor_right = 0.5
offset_left = -300.0
offset_top = 40.0
offset_right = 300.0
offset_bottom = 90.0
theme_override_font_sizes/font_size = 28
text = "موتور بازی‌سازی خلیج فارس"
horizontal_alignment = 1

[node name="CenterContainer" type="VBoxContainer" parent="."]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -160.0
offset_top = -100.0
offset_right = 160.0
offset_bottom = 140.0
theme_override_constants/separation = 16

[node name="BtnNewProject" type="Button" parent="CenterContainer"]
custom_minimum_size = Vector2(0, 48)
layout_mode = 2
text = "ساخت پروژه جدید"

[node name="BtnOpenProject" type="Button" parent="CenterContainer"]
custom_minimum_size = Vector2(0, 48)
layout_mode = 2
text = "پروژه‌های من"

[node name="BtnVisualScript" type="Button" parent="CenterContainer"]
custom_minimum_size = Vector2(0, 48)
layout_mode = 2
text = "ویرایشگر نودهای بصری"

[node name="BtnSwitchLang" type="Button" parent="CenterContainer"]
custom_minimum_size = Vector2(0, 44)
layout_mode = 2
text = "تغییر زبان (English / فارسی)"
""",

    "scripts/editor/main_menu.gd": """extends Control

func _ready() -> void:
    $CenterContainer/BtnNewProject.pressed.connect(_on_new_project_pressed)
    $CenterContainer/BtnOpenProject.pressed.connect(_on_open_project_pressed)
    $CenterContainer/BtnVisualScript.pressed.connect(_on_visual_script_pressed)
    $CenterContainer/BtnSwitchLang.pressed.connect(_on_switch_lang_pressed)

func _on_new_project_pressed() -> void:
    Global.current_project_name = "NewGame_" + str(Time.get_unix_time_from_system())
    Global.current_scene_data = {"objects": []}
    get_tree().change_scene_to_file("res://scenes/editor.tscn")

func _on_open_project_pressed() -> void:
    get_tree().change_scene_to_file("res://scenes/editor.tscn")

func _on_visual_script_pressed() -> void:
    get_tree().change_scene_to_file("res://scenes/visual_scripting_editor.tscn")

func _on_switch_lang_pressed() -> void:
    if LocaleManager.current_locale == "fa":
        LocaleManager.set_language("en")
        $HeaderLabel.text = "Game Engine Persian Gulf"
        $CenterContainer/BtnNewProject.text = "New Project"
        $CenterContainer/BtnOpenProject.text = "Open Project"
        $CenterContainer/BtnVisualScript.text = "Visual Scripting"
    else:
        LocaleManager.set_language("fa")
        $HeaderLabel.text = "موتور بازی‌سازی خلیج فارس"
        $CenterContainer/BtnNewProject.text = "ساخت پروژه جدید"
        $CenterContainer/BtnOpenProject.text = "پروژه‌های من"
        $CenterContainer/BtnVisualScript.text = "ویرایشگر نودهای بصری"
""",

    # 5. محیط اصلی ویرایشگر (Editor Scene & Script)
    "scenes/editor.tscn": """[gd_scene load_steps=2 format=3 uid="uid://editor002"]

[ext_resource type="Script" path="res://scripts/editor/editor_controller.gd" id="1_edit"]

[node name="Editor" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1_edit")

[node name="MainLayout" type="HSplitContainer" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0

[node name="LeftToolbox" type="VBoxContainer" parent="MainLayout"]
custom_minimum_size = Vector2(220, 0)
layout_mode = 2
theme_override_constants/separation = 8

[node name="ToolsLabel" type="Label" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "ابزارهای بازی"
horizontal_alignment = 1

[node name="BtnAddBox" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "افزودن شیء مکعبی (Box)"

[node name="BtnAddCircle" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "افزودن شیء دایره‌ای (Circle)"

[node name="BtnAddLight" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "افزودن نور (Point Light)"

[node name="HSeparator" type="HSeparator" parent="MainLayout/LeftToolbox"]
layout_mode = 2

[node name="BtnPlay" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "تست و اجرای بازی (Play)"

[node name="BtnSave" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "ذخیره صحنه (Save)"

[node name="BtnBack" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "بازگشت به منو"

[node name="GameViewportContainer" type="SubViewportContainer" parent="MainLayout"]
layout_mode = 2
size_flags_horizontal = 3
stretch = true

[node name="SubViewport" type="SubViewport" parent="MainLayout/GameViewportContainer"]
handle_input_locally = true
physics_object_picking = true
size = Vector2i(1050, 720)
render_target_update_mode = 3

[node name="SceneRoot" type="Node2D" parent="MainLayout/GameViewportContainer/SubViewport"]

[node name="Camera2D" type="Camera2D" parent="MainLayout/GameViewportContainer/SubViewport/SceneRoot"]
position = Vector2(525, 360)
""",

    "scripts/editor/editor_controller.gd": """extends Control

@onready var scene_root: Node2D = $MainLayout/GameViewportContainer/SubViewport/SceneRoot
@onready var btn_add_box: Button = $MainLayout/LeftToolbox/BtnAddBox
@onready var btn_add_circle: Button = $MainLayout/LeftToolbox/BtnAddCircle
@onready var btn_add_light: Button = $MainLayout/LeftToolbox/BtnAddLight
@onready var btn_play: Button = $MainLayout/LeftToolbox/BtnPlay
@onready var btn_save: Button = $MainLayout/LeftToolbox/BtnSave
@onready var btn_back: Button = $MainLayout/LeftToolbox/BtnBack

func _ready() -> void:
    btn_add_box.pressed.connect(_on_add_box)
    btn_add_circle.pressed.connect(_on_add_circle)
    btn_add_light.pressed.connect(_on_add_light)
    btn_play.pressed.connect(_on_toggle_play)
    btn_save.pressed.connect(_on_save)
    btn_back.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/main_menu.tscn"))

func _on_add_box() -> void:
    var body = RigidBody2D.new()
    var col = CollisionShape2D.new()
    var shape = RectangleShape2D.new()
    shape.size = Vector2(64, 64)
    col.shape = shape
    
    var visual = ColorRect.new()
    visual.size = Vector2(64, 64)
    visual.position = Vector2(-32, -32)
    visual.color = Color(0.2, 0.6, 0.9)
    
    body.add_child(visual)
    body.add_child(col)
    body.position = Vector2(randf_range(200, 800), 200)
    body.freeze = not Global.is_playing_preview
    scene_root.add_child(body)

func _on_add_circle() -> void:
    var body = RigidBody2D.new()
    var col = CollisionShape2D.new()
    var shape = CircleShape2D.new()
    shape.radius = 32.0
    col.shape = shape
    
    body.add_child(col)
    body.position = Vector2(randf_range(200, 800), 200)
    body.freeze = not Global.is_playing_preview
    scene_root.add_child(body)

func _on_add_light() -> void:
    var light = PointLight2D.new()
    light.color = Color(1.0, 0.85, 0.5)
    light.energy = 1.5
    light.position = Vector2(500, 300)
    scene_root.add_child(light)

func _on_toggle_play() -> void:
    Global.is_playing_preview = not Global.is_playing_preview
    btn_play.text = "توقف بازی (Stop)" if Global.is_playing_preview else "تست و اجرای بازی (Play)"
    for child in scene_root.get_children():
        if child is RigidBody2D:
            child.freeze = not Global.is_playing_preview

func _on_save() -> void:
    Global.save_project()
""",

    # 6. سیستم نودهای اسکریپت‌نویسی بصری (Visual Node Scripting)
    "scenes/visual_scripting_editor.tscn": """[gd_scene load_steps=2 format=3 uid="uid://vis003"]

[ext_resource type="Script" path="res://scripts/visual_script/visual_graph_editor.gd" id="1_vis"]

[node name="VisualScriptEditor" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
script = ExtResource("1_vis")

[node name="VBox" type="VBoxContainer" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0

[node name="TopBar" type="HBoxContainer" parent="VBox"]
custom_minimum_size = Vector2(0, 48)
layout_mode = 2

[node name="BtnBack" type="Button" parent="VBox/TopBar"]
layout_mode = 2
text = "بازگشت"

[node name="BtnAddEvent" type="Button" parent="VBox/TopBar"]
layout_mode = 2
text = "+ رویداد (OnTouch / Collision)"

[node name="BtnAddAction" type="Button" parent="VBox/TopBar"]
layout_mode = 2
text = "+ اکشن (حرکت / نیرو)"

[node name="GraphEdit" type="GraphEdit" parent="VBox"]
layout_mode = 2
size_flags_vertical = 3
right_disconnects = true
""",

    "scripts/visual_script/visual_graph_editor.gd": """extends Control

@onready var graph: GraphEdit = $VBox/GraphEdit
@onready var btn_add_event: Button = $VBox/TopBar/BtnAddEvent
@onready var btn_add_action: Button = $VBox/TopBar/BtnAddAction
@onready var btn_back: Button = $VBox/TopBar/BtnBack

func _ready() -> void:
    btn_add_event.pressed.connect(_on_add_event_node)
    btn_add_action.pressed.connect(_on_add_action_node)
    btn_back.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/main_menu.tscn"))
    graph.connection_request.connect(_on_connection_request)
    graph.disconnection_request.connect(_on_disconnection_request)

func _on_add_event_node() -> void:
    var node = GraphNode.new()
    node.title = "رویداد: هنگام برخورد (OnCollide)"
    node.position_offset = Vector2(100, 150)
    node.set_slot(0, false, 0, Color.WHITE, true, 0, Color.GREEN)
    
    var label = Label.new()
    label.text = "خروجی رویداد ->"
    node.add_child(label)
    graph.add_child(node)

func _on_add_action_node() -> void:
    var node = GraphNode.new()
    node.title = "اکشن: اعمال نیرو (Apply Impulse)"
    node.position_offset = Vector2(400, 150)
    node.set_slot(0, true, 0, Color.GREEN, false, 0, Color.WHITE)
    
    var label = Label.new()
    label.text = "<- ورودی اجرا"
    node.add_child(label)
    graph.add_child(node)

func _on_connection_request(from_node: StringName, from_port: int, to_node: StringName, to_port: int) -> void:
    graph.connect_node(from_node, from_port, to_node, to_port)

func _on_disconnection_request(from_node: StringName, from_port: int, to_node: StringName, to_port: int) -> void:
    graph.disconnect_node(from_node, from_port, to_node, to_port)
"""
}

def build_project():
    for file_path, content in files_to_create.items():
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ ساخت فایل: {file_path}")
    print("\n🎉 تمامی فایل‌ها و ساختار پروژه گودوت با موفقیت ساخته شد!")

if __name__ == "__main__":
    build_project()
