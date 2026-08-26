extends Node

var current_project_name: String = "My3DGamePro"
var current_project_path: String = "user://projects/My3DGamePro/"
var current_scene_data: Dictionary = {
	"objects": [],
	"camera": {"fov": 75.0},
	"physics": {"gravity": 980.0}
}
var is_playing_preview: bool = false
var exporter: Node

func _ready() -> void:
	var exporter_script = load("res://scripts/editor/project_exporter.gd")
	if exporter_script:
		exporter = exporter_script.new()
		add_child(exporter)
	ensure_directories()

func ensure_directories() -> void:
	if not DirAccess.dir_exists_absolute(current_project_path):
		DirAccess.make_dir_recursive_absolute(current_project_path)

func save_project(scene_objects: Array) -> bool:
	ensure_directories()
	current_scene_data["objects"] = scene_objects
	if exporter and exporter.has_method("export_project_to_storage"):
		return exporter.export_project_to_storage(current_project_path, current_scene_data)
	return false

func load_project() -> Array:
	var file_path = current_project_path + "project_data.json"
	if FileAccess.file_exists(file_path):
		var file = FileAccess.open(file_path, FileAccess.READ)
		if file != null:
			var content = file.get_as_text()
			file.close()
			var json = JSON.parse_string(content)
			if json != null and json is Dictionary and json.has("objects"):
				current_scene_data = json
				return json["objects"]
	return []
