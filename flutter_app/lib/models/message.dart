class Message {
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final String? audioUrl;

  Message({
    required this.text,
    required this.isUser,
    DateTime? timestamp,
    this.audioUrl,
  }) : timestamp = timestamp ?? DateTime.now();
}
