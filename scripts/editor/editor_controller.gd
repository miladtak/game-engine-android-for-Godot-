extends Control

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
