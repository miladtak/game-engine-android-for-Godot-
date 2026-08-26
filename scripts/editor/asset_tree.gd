extends Tree

signal file_selected(file_name: String)

func _ready() -> void:
	hide_root = true
	var root = create_item()
	_create_folder(root, "3D Scenes", ["Main World", "Level 1"])
	_create_folder(root, "3D Scripts", ["PlayerMovement3D"])
	_create_folder(root, "Textures", ["Brick_Diffuse", "Wood_Texture"])
	_create_folder(root, "Sound", ["BGM_3D", "SFX"])
	item_selected.connect(_on_item_clicked)

func _create_folder(parent: TreeItem, folder_name: String, files: Array) -> void:
	var folder = create_item(parent)
	folder.set_text(0, folder_name)
	for file in files:
		var file_item = create_item(folder)
		file_item.set_text(0, file)

func _on_item_clicked() -> void:
	var selected = get_selected()
	if selected:
		emit_signal("file_selected", selected.get_text(0))
