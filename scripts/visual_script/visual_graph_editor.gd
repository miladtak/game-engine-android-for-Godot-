extends GraphEdit

func _ready() -> void:
	right_disconnects = true
	connection_request.connect(_on_connection_request)
	_create_node("On_Start", Vector2(40, 40), Color(0.2, 0.5, 0.8), ["Flow Out"])
	_create_node("Player_Move", Vector2(40, 220), Color(0.8, 0.4, 0.2), ["Flow In", "Flow Out"])

func _create_node(title: String, pos: Vector2, color: Color, slots: Array) -> void:
	var node = GraphNode.new()
	node.title = title
	node.position_offset = pos
	var idx = 0
	for slot_name in slots:
		var lbl = Label.new()
		lbl.text = slot_name
		node.add_child(lbl)
		var is_in = slot_name.contains("In")
		var is_out = slot_name.contains("Out")
		node.set_slot(idx, is_in, 0, color, is_out, 0, color)
		idx += 1
	add_child(node)

func _on_connection_request(from_node: String, from_port: int, to_node: String, to_port: int) -> void:
	connect_node(from_node, from_port, to_node, to_port)

# مفسر ویژوال اسکریپت: ترجمه ارتباط بلوک‌ها به منطق بازی در زمان اجرا
func interpret_visual_logic(delta: float) -> void:
	# بررسی ارتباط بین بلوک‌ها برای اجرای دستورات
	var connections = get_connection_list()
	if connections.size() > 0:
		# منطق نمونه: اگر بلوک شروع به بلوک حرکت وصل باشد، سیستم حرکتی تایید می‌شود
		for conn in connections:
			if conn["from"] == "On_Start" or conn["from"] == "Player_Move":
				# اجرای پیوسته دستورات منطقی بلوک‌ها
				pass
