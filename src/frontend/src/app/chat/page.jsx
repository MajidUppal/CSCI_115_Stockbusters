'use client';

import { useState, use, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ChatInput from '@/components/chat/ChatInput';
import ChatHistory from '@/components/chat/ChatHistory';
import ChatHistorySidebar from '@/components/chat/ChatHistorySidebar';
import ChatMessage from '@/components/chat/ChatMessage';
import DataService from "../../lib/DataService";
import { uuid } from "../../lib/Common";

const MODEL = 'llm'; // Single model constant

export default function ChatPage({ searchParams }) {
    const params = use(searchParams);
    const chat_id = params.id;
    console.log(chat_id);

    // Component States
    const [chatId, setChatId] = useState(params.id);
    const [hasActiveChat, setHasActiveChat] = useState(false);
    const [chat, setChat] = useState(null);
    const [refreshKey, setRefreshKey] = useState(0);
    const [isTyping, setIsTyping] = useState(false);
    const [canGenerateReport, setCanGenerateReport] = useState(false);
    const router = useRouter();

    const fetchChat = async (id) => {
        try {
            setChat(null);
            const response = await DataService.GetChat(MODEL, id);
            setChat(response.data);
            console.log(chat);
        } catch (error) {
            console.error('Error fetching chat:', error);
            setChat(null);
        }
    };

    // Setup Component
    useEffect(() => {
        if (chat_id) {
            fetchChat(chat_id);
            setHasActiveChat(true);
        } else {
            setChat(null);
            setHasActiveChat(false);
        }
    }, [chat_id]);

    // Check if report can be generated based on chat messages
    useEffect(() => {
        if (chat && chat.messages && chat.messages.length > 0) {
            // Check if any assistant message contains trigger phrase for report generation
            const reportTriggers = [
                'please press generate report button',
                'press generate report button',
                'click generate report',
                'generate report button',
                'ready to generate report',
                'you can now generate the report'
            ];
            
            const hasReportTrigger = chat.messages.some(msg => 
                msg.role === 'assistant' && 
                reportTriggers.some(trigger => 
                    msg.content.toLowerCase().includes(trigger.toLowerCase())
                )
            );
            
            setCanGenerateReport(hasReportTrigger);
        } else {
            setCanGenerateReport(false);
        }
    }, [chat]);

    function tempChatMessage(message) {
        // Set temp values
        message["message_id"] = uuid();
        message["role"] = 'user';
        if (chat) {
            // Append message
            var temp_chat = { ...chat };
            temp_chat["messages"].push(message);
            return temp_chat;
        } else {
            var temp_chat = {
                "messages": [message]
            }
            return temp_chat;
        }
    }

    // Handlers
    const newChat = (message) => {
        console.log(message);
        // Start a new chat and submit to LLM
        const startChat = async (message) => {
            try {
                // Show typing indicator
                setIsTyping(true);
                setHasActiveChat(true);

                // Submit chat
                const response = await DataService.StartChatWithLLM(MODEL, message);
                console.log(response.data);

                // Hide typing indicator and add response
                setIsTyping(false);

                setChat(response.data);
                setChatId(response.data["chat_id"]);
                router.push('/chat?id=' + response.data["chat_id"]);
            } catch (error) {
                console.error('Error fetching chat:', error);
                setIsTyping(false);
                setChat(null);
                setChatId(null);
                setHasActiveChat(false);
                router.push('/chat')
            }
        };
        startChat(message);

    };
    const appendChat = (message) => {
        console.log(message);
        // Append message and submit to LLM

        const continueChat = async (id, message) => {
            try {
                // Show typing indicator
                setIsTyping(true);
                setHasActiveChat(true);

                // Submit chat
                const response = await DataService.ContinueChatWithLLM(MODEL, id, message);
                console.log(response.data);

                // Hide typing indicator and add response
                setIsTyping(false);

                setChat(response.data);
                forceRefresh();
            } catch (error) {
                console.error('Error fetching chat:', error);
                setIsTyping(false);
                setChat(null);
                setHasActiveChat(false);
            }
        };
        continueChat(chat_id, message);
    };
    // Force re-render by updating the key
    const forceRefresh = () => {
        setRefreshKey(prevKey => prevKey + 1);
    };

    const handleGenerateReport = () => {
        if (!canGenerateReport) return;
        
        console.log('Generating report for chat:', chatId);
        // Add your report generation logic here
        // Example: Call API endpoint to generate report
        // DataService.GenerateReport(MODEL, chatId).then(response => {
        //     console.log('Report generated:', response);
        // });
    };

    return (
        <div className="h-screen flex flex-col">
            {!hasActiveChat ? (
                <>
                    {/* Hero Section */}
                    <section className="flex-shrink-0 min-h-[400px] flex items-center justify-center bg-gradient-to-br from-primary/10 via-primary/5 to-accent">
                        <div className="absolute inset-0 bg-gradient-to-r from-primary/10 via-primary/5 to-transparent" />
                        <div className="container mx-auto px-4 max-w-3xl relative z-10 pt-20">
                            <div className="text-center">
                                <h1 className="text-4xl md:text-6xl font-bold gradient-text mb-6">
                                    AI SmartInvestor 🌟
                                </h1>
                                <div className="bg-card/80 backdrop-blur-lg rounded-xl shadow-lg p-6 border border-border">
                                    <ChatInput onSendMessage={newChat} />
                                </div>
                            </div>
                        </div>
                    </section>

                    {/* Chat History Section */}
                    <div className="flex-1 container mx-auto px-4 py-12 overflow-auto z-10">
                        <ChatHistory />
                    </div>
                </>
            ) : (
                <div className="flex h-[calc(100vh-64px)]">
                    {/* Sidebar */}
                    <div className="w-80 flex-shrink-0 bg-card border-r border-border">
                        <ChatHistorySidebar chat_id={chat_id} />
                    </div>

                    {/* Main Chat Area */}
                    <div className="flex-1 flex flex-col h-full overflow-hidden">
                        {/* Header with Generate Report Button */}
                        <div className="flex-shrink-0 border-b border-border bg-card p-4 flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <h2 className="text-foreground font-medium">
                                    {chat?.title || 'Chat'}
                                </h2>
                            </div>
                            <button
                                onClick={handleGenerateReport}
                                disabled={!canGenerateReport}
                                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                                    canGenerateReport
                                        ? 'bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm hover:shadow-md cursor-pointer'
                                        : 'bg-muted text-muted-foreground cursor-not-allowed opacity-50'
                                }`}
                            >
                                Generate Report
                            </button>
                        </div>

                        <div className="flex-1 overflow-y-auto">
                            <ChatMessage
                                chat={chat}
                                key={refreshKey}
                                isTyping={isTyping}
                            />
                        </div>
                        <div className="flex-shrink-0 border-t border-border bg-card">
                            <ChatInput onSendMessage={appendChat} chat={chat} />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}