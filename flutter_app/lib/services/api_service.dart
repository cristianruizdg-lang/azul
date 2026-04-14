import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';

class ApiService extends ChangeNotifier {
  static const String baseUrl = 'https://azul-4xsp.onrender.com';
  String? _version;
  bool _isConnected = false;
  
  String? get version => _version;
  bool get isConnected => _isConnected;

  // Verificar salud del backend
  Future<bool> checkHealth() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/health'),
      ).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _version = data['version'];
        _isConnected = true;
        notifyListeners();
        return true;
      }
    } catch (e) {
      debugPrint('Error en health check: $e');
      _isConnected = false;
      notifyListeners();
    }
    return false;
  }

  // Enviar mensaje de texto
  Future<Map<String, dynamic>?> sendTextMessage(String text, String userId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/chat/message'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'message': text,
          'user_id': userId,
        }),
      ).timeout(const Duration(seconds: 30));

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      debugPrint('Error enviando mensaje: $e');
    }
    return null;
  }

  // Enviar audio
  Future<Map<String, dynamic>?> sendAudioMessage(String audioPath, String userId) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/api/chat/voice'),
      );

      request.fields['user_id'] = userId;
      request.files.add(await http.MultipartFile.fromPath('audio', audioPath));

      final streamedResponse = await request.send().timeout(const Duration(seconds: 60));
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      debugPrint('Error enviando audio: $e');
    }
    return null;
  }

  // Descargar audio de respuesta
  Future<String?> downloadAudio(String audioUrl) async {
    try {
      // Normalizar URL
      String fullUrl = audioUrl;
      if (audioUrl.startsWith('/')) {
        fullUrl = '$baseUrl$audioUrl';
      }

      final response = await http.get(Uri.parse(fullUrl));
      
      if (response.statusCode == 200) {
        final directory = await getTemporaryDirectory();
        final timestamp = DateTime.now().millisecondsSinceEpoch;
        final filePath = '${directory.path}/azul_response_$timestamp.mp3';
        
        final file = File(filePath);
        await file.writeAsBytes(response.bytes);
        return filePath;
      }
    } catch (e) {
      debugPrint('Error descargando audio: $e');
    }
    return null;
  }

  // Obtener historial
  Future<List<Map<String, dynamic>>> getHistory(String userId, {int limit = 50}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/memory/history?user_id=$userId&limit=$limit'),
      ).timeout(const Duration(seconds: 15));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return List<Map<String, dynamic>>.from(data['history'] ?? []);
      }
    } catch (e) {
      debugPrint('Error obteniendo historial: $e');
    }
    return [];
  }
}
