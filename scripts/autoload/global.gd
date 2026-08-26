extends Node

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
