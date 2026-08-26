extends Control

@onready var scene_root: Node2D = $MainVBox/MainSplit/RightSplit/ViewportPanel/SubViewportContainer/SubViewport/SceneRoot
@onready var play_mode_btn: Button = $MainVBox/TopBar/PlayModeBtn
@onready var btn_export_apk: Button = $MainVBox/TopBar/BtnExportAPK

# پنل‌های ادیتور برای مخفی شدن در حالت تست تمام‌صفحه
@onready var left_panel: PanelContainer = $MainVBox/MainSplit/LeftPanel
@onready var inspector_panel: PanelContainer = $MainVBox/MainSplit/RightSplit/InspectorPanel

# دکمه‌های ابزار
@onready var btn_add_box: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddBox
@onready var btn_add_player: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddPlayer
@onready var btn_add_ground: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddGround
@onready var btn_add_touch_btn: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnAddTouchBtn
@onready var btn_save: Button = $MainVBox/MainSplit/LeftPanel/VBox/BtnSave

@onready var input_pos_x: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputPosX
@onready var input_pos_y: LineEdit = $MainVBox/MainSplit/RightSplit/InspectorPanel/VBox/InputPosY
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
					
					if input_pos_x and input_pos_y and child is Node2D:
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
		# اجرای مفسر ویژوال اسکریپت در زمان بازی
		var graph_editor = get_node_or_null("../MainVBox/MainSplit/RightSplit/GraphPanel/VisualGraphEditor")
		if graph_editor and graph_editor.has_method("interpret_visual_logic"):
			graph_editor.interpret_visual_logic(delta)

		# کنترل فیزیک کاراکتر
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
	
	# حالت تست تمام‌صفحه (مخفی کردن پنل‌های ادیتور در هنگام پلی)
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
		print("فایل خروجی APK درخواست شد.")

func _on_apply_properties() -> void:
	if selected_node != null and selected_node is Node2D:
		var new_x = input_pos_x.text.to_float()
		var new_y = input_pos_y.text.to_float()
		selected_node.global_position = Vector2(new_x, new_y)

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
	if Global.save_project():
		print("پروژه با موفقیت ذخیره شد.")
