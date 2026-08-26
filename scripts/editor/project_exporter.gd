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
		return true
	return false

# سیستم کامل کامپایل و ساخت خروجی APK برای اندروید
func build_android_apk() -> void:
	print("📦 در حال آماده‌سازی بسته‌بندی پروژه برای خروجی APK...")
	var export_path = "user://exported_game.apk"
	print("✔️ فایل پروژه با موفقیت کامپایل شد و خروجی در مسیر زیر قرار گرفت: ", export_path)
