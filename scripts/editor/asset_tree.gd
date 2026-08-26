extends Tree

signal file_selected(file_name: String)

func _ready() -> void:
	hide_root = true
	var root = create_item()
	_create_folder(root, "Scenes", ["Main Level", "Start Screen"])
	_create_folder(root, "Scripts", ["PlayerControl", "AIBehavior"])
	_create_folder(root, "Textures", ["CharacterSprites", "Environment"])
	_create_folder(root, "Sound", ["BGM", "SFX"])
	_create_folder(root, "Items", ["Item_Bag", "Item_Type"])
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
