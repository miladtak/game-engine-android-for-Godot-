extends Node

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
        file.store_string(JSON.stringify(current_scene_data, "\t"))
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
