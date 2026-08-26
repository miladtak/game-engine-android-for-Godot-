extends Node
class_name ProjectExporter

# ذخیره اطلاعات بازی ساخته شده در یک پوشه یا فایل ZIP
func export_project_to_storage(project_name: String, scene_data: Dictionary) -> bool:
	var dir_path = "user://projects/" + project_name
	var dir = Directory.new()
	
	if not dir.dir_exists(dir_path):
		dir.make_dir_recursive(dir_path)
	
	# ذخیره دیتا به صورت JSON
	var file = File.new()
	var err = file.open(dir_path + "/main_scene.json", File.WRITE)
	if err == OK:
		file.store_string(to_json(scene_data))
		file.close()
		print("پروژه با موفقیت ذخیره شد:", dir_path)
		return true
	else:
		print("خطا در ذخیره‌سازی پروژه!")
		return false

# اجرای مستقیم بازی داخل ادیتور روی اندروید
func run_runtime_preview(scene_data: Dictionary, root_node: Node):
	# ساخت نودها به صورت دینامیک بر اساس دیتای ذخیره شده
	for item in scene_data.get("nodes", []):
		var new_node = Sprite.new()
		if item.has("texture_path"):
			new_node.texture = load(item["texture_path"])
		new_node.position = Vector2(item["x"], item["y"])
		root_node.add_child(new_node)
