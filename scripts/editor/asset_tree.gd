extends Tree

func _ready() -> void:
	# پیکربندی ظاهر درختی
	hide_root = true
	var root = create_item()
	
	# ساخت ساختار پوشه‌های موتور
	_create_folder(root, "Scenes", ["Main Level", "Start Screen"])
	_create_folder(root, "Scripts", ["PlayerControl", "AIBehavior"])
	_create_folder(root, "Textures", ["CharacterSprites", "Environment"])
	_create_folder(root, "Sound", ["BGM", "SFX"])
	_create_folder(root, "Plugins", ["AI_Behavior_Pack", "Cutscene_Creator"])
	_create_folder(root, "Items", ["Item_Bag", "Item_Type"])

func _create_folder(parent: TreeItem, folder_name: String, files: Array) -> void:
	var folder = create_item(parent)
	folder.set_text(0, folder_name)
	
	for file in files:
		var file_item = create_item(folder)
		file_item.set_text(0, file)
