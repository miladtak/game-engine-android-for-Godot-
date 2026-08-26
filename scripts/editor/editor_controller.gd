extends Control

@onready var scene_root: Node2D = $MainLayout/GameViewportContainer/SubViewport/SceneRoot
@onready var btn_add_box: Button = $MainLayout/LeftToolbox/BtnAddBox
@onready var btn_add_circle: Button = $MainLayout/LeftToolbox/BtnAddCircle
@onready var btn_add_light: Button = $MainLayout/LeftToolbox/BtnAddLight
@onready var btn_play: Button = $MainLayout/LeftToolbox/BtnPlay
@onready var btn_save: Button = $MainLayout/LeftToolbox/BtnSave
@onready var btn_back: Button = $MainLayout/LeftToolbox/BtnBack

# سیستم جابه‌جایی با تاچ (مخصوص اندروید)
var selected_node: Node2D = null
var is_dragging: bool = false
var drag_offset: Vector2 = Vector2.ZERO

func _ready() -> void:
	btn_add_box.pressed.connect(_on_add_box)
	btn_add_circle.pressed.connect(_on_add_circle)
	btn_add_light.pressed.connect(_on_add_light)
	btn_play.pressed.connect(_on_toggle_play)
	btn_save.pressed.connect(_on_save)
	btn_back.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/main_menu.tscn"))

func _input(event: InputEvent) -> void:
	# اگر بازی در حال اجرا/تست باشد، جابه‌جایی دستی غیرفعال شود
	if Global.is_playing_preview:
		return
		
	# کنترل جابه‌جایی اشیا با لمس صفحه گوشی (Touch Event)
	if event is InputEventScreenTouch:
		if event.pressed:
			for child in scene_root.get_children():
				if child is Node2D:
					# بررسی فاصله لمس تا مرکز شیء برای انتخاب آن
					if event.position.distance_to(child.global_position) < 50.0:
						selected_node = child
						is_dragging = true
						drag_offset = child.global_position - event.position
						break
		else:
			is_dragging = false
			selected_node = null
			
	elif event is InputEventScreenDrag and is_dragging:
		if selected_node:
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
	
	# ساخت نمایش گرافیکی دایره جهت دیده شدن روی گوشی
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
	btn_play.text = "توقف بازی (Stop)" if Global.is_playing_preview else "تست و اجرای بازی (Play)"
	
	for child in scene_root.get_children():
		if child is RigidBody2D:
			child.freeze = not Global.is_playing_preview

func _on_save() -> void:
	# استخراج اطلاعات کامل صحنه جهت ذخیره روی حافظه موبایل
	var scene_data: Array = []
	for child in scene_root.get_children():
		var item_data = {
			"name": child.name,
			"position_x": child.position.x,
			"position_y": child.position.y,
			"type": child.get_class()
		}
		scene_data.append(item_data)
	
	# فراخوانی تابع ذخیره در Autoload
	if Global.has_method("save_project"):
		Global.save_project(scene_data)
	else:
		Global.save_project()
	
	print("پروژه با موفقیت ذخیره شد!")
