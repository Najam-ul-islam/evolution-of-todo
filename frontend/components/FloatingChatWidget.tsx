'use client';

import { useState, useEffect } from 'react';
import authService from '../services/authService';
import { sendAuthenticatedMessage } from '../services/chat-api';

interface FloatingChatWidgetProps {
  domainKey?: string;
}

const FloatingChatWidget: React.FC<FloatingChatWidgetProps> = ({ domainKey = process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || '' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [error, setError] = useState<string | null>(null);
  const [messages, setMessages] = useState<Array<{id: string; text: string; sender: string; timestamp: string}>>([]);
  const [inputValue, setInputValue] = useState('');
  const [session, setSession] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

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

  // Restore conversation from localStorage
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedId = localStorage.getItem('current_conversation_id');
      if (storedId) setConversationId(storedId);
    }
  }, []);

  // Handle sending messages
  const handleSendMessage = async () => {
    if (!inputValue.trim() || !session?.id) return;

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

      const response = await sendAuthenticatedMessage(
        { message: currentInput, conversation_id: conversationId },
        session.id,
        token || ''
      );

      if (response.conversation_id !== conversationId) {
        setConversationId(response.conversation_id);
        if (typeof window !== 'undefined') {
          localStorage.setItem('current_conversation_id', response.conversation_id);
        }
      }

      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        text: response.response,
        sender: 'assistant',
        timestamp: new Date().toISOString(),
      }]);
    } catch (err) {
      console.error('Error sending message:', err);
      let errorMessage = 'Failed to send message';

      if (err instanceof Error) {
        if (err.message.includes('No authentication token')) {
          errorMessage = 'Authentication required. Please log in again.';
        } else if (err.message.includes('fetch')) {
          errorMessage = 'Network error. Please check your connection.';
        } else if (err.message.includes('Conversation not found')) {
          errorMessage = 'Starting a new conversation.';
          setConversationId(undefined);
          if (typeof window !== 'undefined') {
            localStorage.removeItem('current_conversation_id');
          }
        } else {
          errorMessage = err.message;
        }
        setError(errorMessage);
      }

      setMessages(prev => [...prev, {
        id: (Date.now() + 2).toString(),
        text: `Error: ${errorMessage}`,
        sender: 'system',
        timestamp: new Date().toISOString(),
      }]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Now safely use hydration state in RENDER logic
  if (isLoading) return null;
  if (!session) return null;
  if (!domainKey) {
    return (
      <div className="fixed bottom-6 right-6">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Error: </strong>
          <span className="block sm:inline">OPENAI_DOMAIN_KEY not configured</span>
        </div>
      </div>
    );
  }

  return (
    <>
      {isOpen ? (
        <div className="fixed bottom-24 right-6 z-50 w-96 h-[500px] bg-gradient-to-br from-orange-50 to-pink-50 rounded-2xl shadow-2xl border border-orange-200/50 flex flex-col overflow-hidden backdrop-blur-sm">
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white p-4 flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold">Chat Assistant</h3>
                <p className="text-xs text-white/80 opacity-80">Online now</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white/80 hover:text-white hover:bg-white/20 rounded-full p-1 transition-all duration-200"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Messages Container */}
          <div className="flex-grow p-4 overflow-y-auto space-y-4">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center text-gray-600 p-4">
                <div className="w-12 h-12 bg-gradient-to-r from-orange-400 to-pink-500 rounded-full flex items-center justify-center mb-3 shadow-md">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <h4 className="font-medium text-gray-800 mb-1">Start a conversation</h4>
                <p className="text-sm text-gray-600">Type a message to begin chatting with the assistant</p>
              </div>
            ) : (
              <div className="space-y-3">
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`group flex gap-2 ${
                      msg.sender === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    {msg.sender !== 'user' && (
                      <div className="w-7 h-7 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 shadow-md">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                      </div>
                    )}

                    <div
                      className={`max-w-[80%] rounded-2xl p-3 shadow-md transition-all duration-200 ${
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
                      <div className={`text-xs mt-1 opacity-80 ${
                        msg.sender === 'user' ? 'text-indigo-100' :
                        msg.sender === 'system' ? 'text-red-100' : 'text-orange-600'
                      }`}>
                        {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>

                    {msg.sender === 'user' && (
                      <div className="w-7 h-7 bg-gradient-to-r from-orange-400 to-red-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 shadow-md">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-gradient-to-r from-red-500 to-red-600 text-white px-4 py-2 text-sm">
              <div className="flex items-center justify-between">
                <span className="font-medium">Error: {error}</span>
                <button onClick={() => setError(null)} className="text-white hover:text-gray-200 ml-2">
                  ×
                </button>
              </div>
            </div>
          )}

          {/* Input Area */}
          <div className="p-4 border-t border-purple-400/60 bg-gradient-to-b from-purple-200 to-pink-300/90 backdrop-blur-sm">
            <div className="flex space-x-3">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type a message..."
                className="flex-grow border-2 border-purple-400 rounded-2xl px-5 py-4 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-gradient-to-r from-purple-200 to-pink-200 font-black text-2xl text-purple-900 placeholder-purple-500"
                rows={1}
                style={{ minHeight: '50px', maxHeight: '120px', fontSize: '1.5rem', lineHeight: '1.5' }}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputValue.trim()}
                className={`px-6 py-4 rounded-2xl font-black text-lg transition-all duration-300 flex items-center justify-center ${
                  inputValue.trim()
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-700 hover:to-pink-700 shadow-2xl hover:shadow-3xl transform hover:-translate-y-1 scale-105'
                    : 'bg-gradient-to-r from-gray-300 to-gray-500 text-gray-600 cursor-not-allowed'
                }`}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 bg-gradient-to-r from-orange-500 to-pink-600 text-white p-4 rounded-full shadow-xl hover:shadow-2xl hover:from-orange-600 hover:to-pink-700 focus:outline-none focus:ring-4 focus:ring-orange-500/30 transition-all duration-300 group"
          aria-label="Open chat"
        >
          <div className="relative">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-white group-hover:animate-pulse"></div>
          </div>
        </button>
      )}
    </>
  );
};

export default FloatingChatWidget;