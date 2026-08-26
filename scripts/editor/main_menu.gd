extends Control

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
