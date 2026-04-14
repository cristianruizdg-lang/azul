import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';
import '../services/audio_service.dart';
import '../widgets/message_bubble.dart';
import '../models/message.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<Message> _messages = [];
  String _userId = 'user_flutter_001';
  bool _isLoading = false;
  String _statusText = 'Conectando...';

  @override
  void initState() {
    super.initState();
    _initialize();
  }

  Future<void> _initialize() async {
    // Cargar user_id de preferencias
    final prefs = await SharedPreferences.getInstance();
    _userId = prefs.getString('user_id') ?? 'user_flutter_${DateTime.now().millisecondsSinceEpoch}';
    await prefs.setString('user_id', _userId);

    // Verificar conexión con backend
    final apiService = context.read<ApiService>();
    final connected = await apiService.checkHealth();
    
    if (mounted) {
      setState(() {
        _statusText = connected 
            ? '✅ Conectado v${apiService.version}' 
            : '❌ Error de conexión';
      });

      if (connected) {
        _loadHistory();
      }
    }
  }

  Future<void> _loadHistory() async {
    final apiService = context.read<ApiService>();
    final history = await apiService.getHistory(_userId, limit: 30);
    
    if (mounted) {
      setState(() {
        _messages.clear();
        for (var item in history.reversed) {
          _messages.add(Message(
            text: item['user_message'] ?? '',
            isUser: true,
            timestamp: DateTime.parse(item['timestamp']),
          ));
          _messages.add(Message(
            text: item['azul_response'] ?? '',
            isUser: false,
            timestamp: DateTime.parse(item['timestamp']),
            audioUrl: item['audio_url'],
          ));
        }
      });
      _scrollToBottom();
    }
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _sendTextMessage() async {
    final text = _textController.text.trim();
    if (text.isEmpty || _isLoading) return;

    _textController.clear();
    
    setState(() {
      _messages.add(Message(text: text, isUser: true));
      _isLoading = true;
      _statusText = 'Enviando...';
    });
    _scrollToBottom();

    final apiService = context.read<ApiService>();
    final response = await apiService.sendTextMessage(text, _userId);

    if (mounted) {
      setState(() {
        _isLoading = false;
        if (response != null) {
          _statusText = '✅ Conectado v${apiService.version}';
          _messages.add(Message(
            text: response['response'] ?? '',
            isUser: false,
            audioUrl: response['audio_url'],
          ));
          
          // Reproducir audio si existe
          if (response['audio_url'] != null) {
            _playResponseAudio(response['audio_url']);
          }
        } else {
          _statusText = '❌ Error al enviar';
        }
      });
      _scrollToBottom();
    }
  }

  Future<void> _sendVoiceMessage() async {
    final audioService = context.read<AudioService>();
    
    if (audioService.isRecording) {
      // Detener grabación
      final audioPath = await audioService.stopRecording();
      if (audioPath == null) return;

      setState(() {
        _messages.add(Message(text: '[Mensaje de voz]', isUser: true));
        _isLoading = true;
        _statusText = 'Enviando audio...';
      });
      _scrollToBottom();

      final apiService = context.read<ApiService>();
      final response = await apiService.sendAudioMessage(audioPath, _userId);

      if (mounted) {
        setState(() {
          _isLoading = false;
          if (response != null) {
            _statusText = '✅ Conectado v${apiService.version}';
            
            // Actualizar último mensaje con transcripción
            if (_messages.isNotEmpty && _messages.last.isUser) {
              _messages.last = Message(
                text: response['transcription'] ?? '[Mensaje de voz]',
                isUser: true,
              );
            }
            
            _messages.add(Message(
              text: response['response'] ?? '',
              isUser: false,
              audioUrl: response['audio_url'],
            ));
            
            if (response['audio_url'] != null) {
              _playResponseAudio(response['audio_url']);
            }
          } else {
            _statusText = '❌ Error al enviar audio';
          }
        });
        _scrollToBottom();
      }
    } else {
      // Iniciar grabación
      final started = await audioService.startRecording();
      if (started && mounted) {
        setState(() {
          _statusText = '🎤 Grabando...';
        });
      }
    }
  }

  Future<void> _playResponseAudio(String audioUrl) async {
    final apiService = context.read<ApiService>();
    final audioService = context.read<AudioService>();
    
    final localPath = await apiService.downloadAudio(audioUrl);
    if (localPath != null) {
      await audioService.playAudio(localPath);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Azul Mobile'),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadHistory,
            tooltip: 'Recargar historial',
          ),
        ],
      ),
      body: Column(
        children: [
          // Status bar
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
            color: Theme.of(context).colorScheme.primary.withOpacity(0.1),
            child: Text(
              _statusText,
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Theme.of(context).colorScheme.primary,
                fontSize: 12,
              ),
            ),
          ),
          
          // Messages list
          Expanded(
            child: _messages.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.chat_bubble_outline,
                          size: 64,
                          color: Theme.of(context).colorScheme.primary.withOpacity(0.5),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Comienza a chatear con Azul',
                          style: TextStyle(
                            color: Colors.white.withOpacity(0.5),
                            fontSize: 16,
                          ),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    itemCount: _messages.length,
                    itemBuilder: (context, index) {
                      return MessageBubble(
                        message: _messages[index],
                        onPlayAudio: _playResponseAudio,
                      );
                    },
                  ),
          ),
          
          // Input area
          Container(
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.3),
                  blurRadius: 8,
                  offset: const Offset(0, -2),
                ),
              ],
            ),
            padding: const EdgeInsets.all(8),
            child: SafeArea(
              child: Row(
                children: [
                  // Voice button
                  Consumer<AudioService>(
                    builder: (context, audioService, _) {
                      return IconButton(
                        icon: Icon(
                          audioService.isRecording ? Icons.stop : Icons.mic,
                          color: audioService.isRecording 
                              ? Colors.red 
                              : Theme.of(context).colorScheme.primary,
                        ),
                        onPressed: _isLoading ? null : _sendVoiceMessage,
                        iconSize: 28,
                      );
                    },
                  ),
                  
                  const SizedBox(width: 8),
                  
                  // Text input
                  Expanded(
                    child: TextField(
                      controller: _textController,
                      enabled: !_isLoading,
                      decoration: InputDecoration(
                        hintText: 'Escribe un mensaje...',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(24),
                          borderSide: BorderSide.none,
                        ),
                        filled: true,
                        fillColor: Theme.of(context).colorScheme.surfaceVariant,
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 20,
                          vertical: 10,
                        ),
                      ),
                      maxLines: null,
                      textCapitalization: TextCapitalization.sentences,
                      onSubmitted: (_) => _sendTextMessage(),
                    ),
                  ),
                  
                  const SizedBox(width: 8),
                  
                  // Send button
                  IconButton(
                    icon: _isLoading
                        ? SizedBox(
                            width: 24,
                            height: 24,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              color: Theme.of(context).colorScheme.primary,
                            ),
                          )
                        : Icon(
                            Icons.send,
                            color: Theme.of(context).colorScheme.primary,
                          ),
                    onPressed: _isLoading ? null : _sendTextMessage,
                    iconSize: 28,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }
}
