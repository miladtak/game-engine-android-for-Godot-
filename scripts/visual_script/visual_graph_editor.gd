extends Control

@onready var graph: GraphEdit = $VBox/GraphEdit
@onready var btn_add_event: Button = $VBox/TopBar/BtnAddEvent
@onready var btn_add_action: Button = $VBox/TopBar/BtnAddAction
@onready var btn_back: Button = $VBox/TopBar/BtnBack

func _ready() -> void:
    btn_add_event.pressed.connect(_on_add_event_node)
    btn_add_action.pressed.connect(_on_add_action_node)
    btn_back.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/main_menu.tscn"))
    graph.connection_request.connect(_on_connection_request)
    graph.disconnection_request.connect(_on_disconnection_request)

func _on_add_event_node() -> void:
    var node = GraphNode.new()
    node.title = "رویداد: هنگام برخورد (OnCollide)"
    node.position_offset = Vector2(100, 150)
    node.set_slot(0, false, 0, Color.WHITE, true, 0, Color.GREEN)
    
    var label = Label.new()
    label.text = "خروجی رویداد ->"
    node.add_child(label)
    graph.add_child(node)

func _on_add_action_node() -> void:
    var node = GraphNode.new()
    node.title = "اکشن: اعمال نیرو (Apply Impulse)"
    node.position_offset = Vector2(400, 150)
    node.set_slot(0, true, 0, Color.GREEN, false, 0, Color.WHITE)
    
    var label = Label.new()
    label.text = "<- ورودی اجرا"
    node.add_child(label)
    graph.add_child(node)

func _on_connection_request(from_node: StringName, from_port: int, to_node: StringName, to_port: int) -> void:
    graph.connect_node(from_node, from_port, to_node, to_port)

func _on_disconnection_request(from_node: StringName, from_port: int, to_node: StringName, to_port: int) -> void:
    graph.disconnect_node(from_node, from_port, to_node, to_port)
