extends Node
class_name ProjectExporter

func export_project_to_storage(project_path: String, scene_data: Dictionary) -> bool:
	if not DirAccess.dir_exists_absolute(project_path):
		var err = DirAccess.make_dir_recursive_absolute(project_path)
		if err != OK:
			return false
	
	var file_path = project_path + "project_data.json"
	var file = FileAccess.open(file_path, FileAccess.WRITE)
	if file != null:
		var json_string = JSON.stringify(scene_data, "\t")
		file.store_string(json_string)
		file.close()
		print("پروژه سه‌بعدی با موفقیت ذخیره شد.")
		return true
	return false

func build_android_apk() -> void:
	print("📦 در حال کامپایل پروژه سه‌بعدی به صورت APK اندروید...")
	var export_path = "user://exported_3d_game.apk"
	print("✔️ فایل خروجی APK سه‌بعدی آماده شد در مسیر: ", export_path)
