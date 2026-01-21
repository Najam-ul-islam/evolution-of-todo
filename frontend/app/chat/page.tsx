'use client';

import { useState, useEffect, useRef } from 'react';
import authService from '../../services/authService';
import { sendAuthenticatedMessage } from '../../services/chat-api';

const ChatPage = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Check current user session on mount
  useEffect(() => {
    const checkSession = async () => {
      setIsLoading(true);
      const result = await authService.getCurrentUser();
      if (result.success) {
        setSession(result.data);
      } else {
        setSession(null);
      }
      setIsLoading(false);
    };

    checkSession();
  }, []);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load conversation from localStorage on mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedId = localStorage.getItem('current_conversation_id');
      if (storedId) {
        setConversationId(storedId);
      }
    }
  }, []);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || !session?.id) return;

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setError(null);

    try {
      // Get the auth token from localStorage
      const token = localStorage.getItem('accessToken');

      // Call the authenticated API
      const response = await sendAuthenticatedMessage({
        message: currentInput,
        conversation_id: conversationId,
      }, session.id, token || '');

      // Update conversation ID if it changed
      if (response.conversation_id !== conversationId) {
        setConversationId(response.conversation_id);
        if (typeof window !== 'undefined') {
          localStorage.setItem('current_conversation_id', response.conversation_id);
        }
      }

      // Add assistant response to messages
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        text: response.response,
        sender: 'assistant',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error sending message:', err);

      let errorMessage = 'Failed to send message';

      if (err instanceof Error) {
        if (err.message.includes('No authentication token')) {
          errorMessage = 'Authentication required. Please log in again.';
          setError('Authentication token is missing. Please log in again.');
        } else if (err.message.includes('fetch')) {
          errorMessage = 'Network error. Please check your connection.';
          setError('Network error: Unable to connect to the server. Please check your connection.');
        } else if (err.message.includes('Conversation not found')) {
          errorMessage = 'Starting a new conversation.';
          setError('Conversation not found. Starting a new conversation.');
          setConversationId(undefined);
          if (typeof window !== 'undefined') {
            localStorage.removeItem('current_conversation_id');
          }
        } else {
          errorMessage = err.message;
          setError(err.message);
        }
      }

      const errorMsg = {
        id: (Date.now() + 1).toString(),
        text: `Error: ${errorMessage}`,
        sender: 'system',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMsg]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Show loading state while loading auth
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p>Loading...</p>
      </div>
    );
  }

  // Show login message if not authenticated
  if (!session) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p>Please log in to access the chat</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-orange-50 via-pink-50 to-purple-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white/90 backdrop-blur-sm border-b border-white/20 shadow-lg sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-yellow-300 to-white bg-clip-text text-transparent">
                Chat Assistant
              </h1>
              <p className="text-sm text-white/80 mt-1">
                Connected as <span className="font-medium text-white">{session.email}</span>
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-sm text-white/80">Online</span>
            </div>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-grow overflow-y-auto p-6 pb-20">
        <div className="max-w-4xl mx-auto space-y-6">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-orange-400 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">Welcome to Chat Assistant!</h3>
                <p className="text-gray-600 max-w-md mx-auto">
                  Start a conversation by typing your message below. I'm here to help you with any questions.
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`group flex gap-3 ${
                    msg.sender === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  {msg.sender !== 'user' && (
                    <div className="w-8 h-8 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-full flex items-center justify-center flex-shrink-0 shadow-md">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                    </div>
                  )}

                  <div
                    className={`max-w-[75%] rounded-2xl p-4 shadow-md transition-all duration-200 ${
                      msg.sender === 'user'
                        ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-br-md shadow-lg'
                        : msg.sender === 'system'
                        ? 'bg-gradient-to-r from-red-400 to-red-500 text-white border border-red-300 rounded-tl-md shadow-md'
                        : 'bg-gradient-to-r from-white to-orange-50 text-orange-900 border border-orange-200 rounded-tl-md shadow-md'
                    }`}
                  >
                    <div className={`whitespace-pre-wrap break-words ${
                      msg.sender === 'user' ? 'text-white' :
                      msg.sender === 'system' ? 'text-white' : 'text-orange-900'
                    }`}>{msg.text}</div>
                    <div className={`text-xs mt-2 opacity-80 ${
                      msg.sender === 'user' ? 'text-indigo-100' :
                      msg.sender === 'system' ? 'text-red-100' : 'text-orange-600'
                    }`}>
                      {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>

                  {msg.sender === 'user' && (
                    <div className="w-8 h-8 bg-gradient-to-r from-orange-400 to-red-500 rounded-full flex items-center justify-center flex-shrink-0 shadow-md">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    </div>
                  )}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="fixed bottom-20 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-red-500 to-red-600 text-white px-6 py-3 rounded-xl shadow-xl z-50 max-w-md mx-4">
          <div className="flex items-center justify-between">
            <span className="font-medium">{error}</span>
            <button
              onClick={() => setError(null)}
              className="ml-4 text-white hover:text-gray-200"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="bg-gradient-to-b from-purple-200 to-pink-300/90 backdrop-blur-sm border-t border-purple-400/60 p-4 sticky bottom-0">
        <div className="max-w-4xl mx-auto">
          <div className="relative flex items-center space-x-3 bg-gradient-to-r from-purple-100 via-pink-100 to-purple-200 rounded-3xl p-5 border-2 border-purple-400 focus-within:border-purple-500 focus-within:shadow-2xl transition-all duration-300 shadow-xl">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here..."
              className="flex-1 bg-gradient-to-r from-purple-200 to-pink-200 border-none outline-none resize-none text-2xl text-purple-900 placeholder-purple-500 min-h-[40px] max-h-40 font-bold"
              rows={1}
              style={{ minHeight: '40px', fontSize: '1.5rem', lineHeight: '1.5' }}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim()}
              className={`px-8 py-4 rounded-2xl font-black text-lg transition-all duration-300 ${
                inputValue.trim()
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-700 hover:to-pink-700 shadow-2xl hover:shadow-3xl transform hover:-translate-y-1.5 scale-110'
                  : 'bg-gradient-to-r from-gray-300 to-gray-500 text-gray-600 cursor-not-allowed'
              }`}
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
          <p className="text-sm text-purple-800 mt-3 text-center font-black bg-gradient-to-r from-purple-200 to-pink-200 px-6 py-2 rounded-full inline-block border-2 border-purple-300 shadow-lg">
            Press Enter to send • Shift+Enter for new line
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;