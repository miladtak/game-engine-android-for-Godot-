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

@onready var scene_root: Node2D = $MainLayout/GameViewportContainer/SubViewport/SceneRoot
@onready var btn_add_box: Button = $MainLayout/LeftToolbox/BtnAddBox
@onready var btn_add_circle: Button = $MainLayout/LeftToolbox/BtnAddCircle
@onready var btn_add_light: Button = $MainLayout/LeftToolbox/BtnAddLight
@onready var btn_play: Button = $MainLayout/LeftToolbox/BtnPlay
@onready var btn_save: Button = $MainLayout/LeftToolbox/BtnSave
@onready var btn_back: Button = $MainLayout/LeftToolbox/BtnBack

# سیستم جابه‌جایی اشیاء با تاچ مخصوص صفحه موبایل
var selected_node: Node2D = null
var is_dragging: bool = false
var drag_offset: Vector2 = Vector2.ZERO

func _ready() -> void:
	if btn_add_box: btn_add_box.pressed.connect(_on_add_box)
	if btn_add_circle: btn_add_circle.pressed.connect(_on_add_circle)
	if btn_add_light: btn_add_light.pressed.connect(_on_add_light)
	if btn_play: btn_play.pressed.connect(_on_toggle_play)
	if btn_save: btn_save.pressed.connect(_on_save)
	if btn_back: btn_back.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/main_menu.tscn"))

func _input(event: InputEvent) -> void:
	if Global.is_playing_preview:
		return
		
	if event is InputEventScreenTouch:
		if event.pressed:
			for child in scene_root.get_children():
				if child is Node2D:
					if event.position.distance_to(child.global_position) < 60.0:
						selected_node = child
						is_dragging = true
						drag_offset = child.global_position - event.position
						break
		else:
			is_dragging = false
			selected_node = null
			
	elif event is InputEventScreenDrag and is_dragging:
		if selected_node != null:
			selected_node.global_position = event.position + drag_offset

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
	
	var visual = Panel.new()
	visual.size = Vector2(64, 64)
	visual.position = Vector2(-32, -32)
	
	body.add_child(visual)
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
	if btn_play:
		btn_play.text = "توقف بازی (Stop)" if Global.is_playing_preview else "تست و اجرای بازی (Play)"
	
	for child in scene_root.get_children():
		if child is RigidBody2D:
			child.freeze = not Global.is_playing_preview

func _on_save() -> void:
	var objects_data: Array = []
	for child in scene_root.get_children():
		if child is Node2D:
			var obj = {
				"type": child.get_class(),
				"position_x": child.position.x,
				"position_y": child.position.y
			}
			objects_data.append(obj)
	
	Global.current_scene_data["objects"] = objects_data
	
	if Global.save_project():
		print("پروژه با موفقیت در سیستم ذخیره شد.")
	else:
		print("خطا در ذخیره‌سازی پروژه.")
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

    "scripts/visual_script/visual_graph_editor.gd": """extends Control
# اسکریپت مربوط به سیستم ویژوال اسکریپتینگ
pass
""",

    "scenes/editor.tscn": """[gd_scene load_steps=2 format=3 uid="uid://editor123"]
[ext_resource type="Script" path="res://scripts/editor/editor_controller.gd" id="1_editor"]

[node name="EditorController" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1_editor")

[node name="MainLayout" type="HBoxContainer" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2

[node name="LeftToolbox" type="VBoxContainer" parent="MainLayout"]
custom_minimum_size = Vector2(150, 0)
layout_mode = 2

[node name="BtnAddBox" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "Add Box"

[node name="BtnAddCircle" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "Add Circle"

[node name="BtnAddLight" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "Add Light"

[node name="BtnPlay" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "Play Game"

[node name="BtnSave" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "Save Project"

[node name="BtnBack" type="Button" parent="MainLayout/LeftToolbox"]
layout_mode = 2
text = "Back to Menu"

[node name="GameViewportContainer" type="SubViewportContainer" parent="MainLayout"]
layout_mode = 2
size_flags_horizontal = 3
stretch = true

[node name="SubViewport" type="SubViewport" parent="MainLayout/GameViewportContainer"]
handle_input_locally = false
size = Vector2i(1002, 648)
render_target_update_mode = 4

[node name="SceneRoot" type="Node2D" parent="MainLayout/GameViewportContainer/SubViewport"]
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
        
    print("\\n✅ پروژه با موفقیت ایجاد شد! حالا می‌توانید آن را در گودوت باز کنید.")

if __name__ == "__main__":
    build_project()
