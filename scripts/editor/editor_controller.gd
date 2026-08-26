extends Control

@onready var scene_root: Node2D = $MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport/SceneRoot
@onready var play_mode_btn: Button = $MainVBox/TopBar/PlayModeBtn

# دکمه‌های ابزار
@onready var btn_add_box: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddBox
@onready var btn_add_player: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddPlayer
@onready var btn_add_ground: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddGround
@onready var btn_save: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnSave

var selected_node: Node2D = null
var is_dragging: bool = false
var drag_offset: Vector2 = Vector2.ZERO

func _ready() -> void:
	if play_mode_btn: play_mode_btn.pressed.connect(_on_toggle_play_mode)
	if btn_add_box: btn_add_box.pressed.connect(_on_add_box)
	if btn_add_player: btn_add_player.pressed.connect(_on_add_player)
	if btn_add_ground: btn_add_ground.pressed.connect(_on_add_ground)
	if btn_save: btn_save.pressed.connect(_on_save_project)

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
	body.position = Vector2(400, 150)
	body.freeze = not Global.is_playing_preview
	scene_root.add_child(body)

func _on_add_player() -> void:
	# ساخت کاراکتر با فیزیک دوبعدی (CharacterBody2D)
	var player = CharacterBody2D.new()
	player.name = "PlayerCharacter"
	
	var col = CollisionShape2D.new()
	var shape = CapsuleShape2D.new()
	shape.radius = 16.0
	shape.height = 48.0
	col.shape = shape
	
	var visual = ColorRect.new()
	visual.size = Vector2(32, 48)
	visual.position = Vector2(-16, -24)
	visual.color = Color(0.9, 0.3, 0.3) # رنگ متمایز برای کاراکتر
	
	player.add_child(visual)
	player.add_child(col)
	player.position = Vector2(400, 200)
	scene_root.add_child(player)
	print("کاراکتر با قابلیت فیزیک اضافه شد.")

func _on_add_ground() -> void:
	# ساخت زمین ثابت (StaticBody2D)
	var ground = StaticBody2D.new()
	ground.name = "GroundPlatform"
	
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(400, 48)
	col.shape = shape
	
	var visual = ColorRect.new()
	visual.size = Vector2(400, 48)
	visual.position = Vector2(-200, -24)
	visual.color = Color(0.3, 0.8, 0.3) # رنگ سبز برای زمین
	
	ground.add_child(visual)
	ground.add_child(col)
	ground.position = Vector2(400, 450)
	scene_root.add_child(ground)
	print("زمین بازی اضافه شد.")

func _on_toggle_play_mode() -> void:
	Global.is_playing_preview = not Global.is_playing_preview
	if Global.is_playing_preview:
		play_mode_btn.text = " توقف بازی (Stop) "
		play_mode_btn.modulate = Color(1, 0.4, 0.4)
	else:
		play_mode_btn.text = " تست و اجرای بازی (Play) "
		play_mode_btn.modulate = Color(1, 1, 1)
		
	for child in scene_root.get_children():
		if child is RigidBody2D:
			child.freeze = not Global.is_playing_preview

func _on_save_project() -> void:
	if Global.save_project():
		print("پروژه با موفقیت ذخیره شد.")
