import { useState, useEffect } from 'react';
import { TrendingUp, Search } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useNavigate, useSearchParams } from 'react-router-dom';

export function RightPanel() {
    const { isDark } = useTheme();
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const [searchTerm, setSearchTerm] = useState(searchParams.get('search') || '');

    // Cập nhật lại search term nếu URL thay đổi (VD user xóa param)
    useEffect(() => {
        setSearchTerm(searchParams.get('search') || '');
    }, [searchParams]);

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            if (searchTerm.trim()) {
                navigate(`/?search=${encodeURIComponent(searchTerm.trim())}`);
            } else {
                navigate('/');
            }
        }
    };

    const cardStyle = {
        background: isDark ? '#1A1A24' : '#FFFFFF',
        boxShadow: isDark
            ? '0 2px 20px rgba(0,0,0,0.25), 0 0 0 1px rgba(255,255,255,0.04)'
            : '0 2px 20px rgba(0,0,0,0.06), 0 0 0 1px rgba(0,0,0,0.04)',
        borderRadius: '16px',
        marginBottom: '12px',
        overflow: 'hidden',
    };

    const trendingTopics = [
        { tag: 'ConfessionDTU', posts: 1240, trend: '+28%' },
        { tag: 'DờiSốngSinhViên', posts: 890, trend: '+15%' },
        { tag: 'TìnhYêu', posts: 670, trend: '+42%' },
        { tag: 'HọcTập', posts: 530, trend: '+8%' },
        { tag: 'KýTúcXá', posts: 320, trend: '+56%' },
    ];

    return (
        <div className="flex flex-col gap-0 w-full">
            {/* Search */}
            <div style={cardStyle}>
                <div className="p-4">
                    <div
                        className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl"
                        style={{
                            background: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(79, 142, 247, 0.06)',
                            border: isDark ? '1px solid rgba(255,255,255,0.06)' : '1px solid rgba(79, 142, 247, 0.12)',
                        }}
                    >
                        <Search size={16} style={{ color: isDark ? '#475569' : '#94A3B8', flexShrink: 0 }} />
                        <input
                            type="text"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Tìm kiếm confession..."
                            className="flex-1 bg-transparent outline-none"
                            style={{
                                fontFamily: 'Inter, sans-serif',
                                fontSize: '0.875rem',
                                color: isDark ? '#F1F5F9' : '#1A1A2E',
                            }}
                        />
                    </div>
                </div>
            </div>

            {/* Trending */}
            <div style={cardStyle}>
                <div className="px-4 pt-4 pb-2">
                    <div className="flex items-center gap-2 mb-3">
                        <TrendingUp size={16} style={{ color: '#C53030' }} />
                        <span
                            style={{
                                fontFamily: 'Poppins, sans-serif',
                                fontWeight: 700,
                                fontSize: '0.9rem',
                                color: isDark ? '#F1F5F9' : '#1A1A2E',
                            }}
                        >
                            Xu hướng
                        </span>
                    </div>
                    <div className="flex flex-col">
                        {trendingTopics.map((topic, i) => (
                            <div
                                key={topic.tag}
                                className="flex items-center justify-between py-2.5 rounded-xl px-2 transition-colors cursor-pointer hover:opacity-80"
                                style={{
                                    borderBottom:
                                        i < trendingTopics.length - 1
                                            ? isDark
                                                ? '1px solid rgba(255,255,255,0.04)'
                                                : '1px solid rgba(0,0,0,0.04)'
                                            : 'none',
                                }}
                            >
                                <div className="flex items-center gap-2.5">
                                    <span
                                        className="w-6 h-6 rounded-lg flex items-center justify-center text-xs"
                                        style={{ background: 'rgba(197, 48, 48, 0.1)', color: '#C53030', fontFamily: 'Inter, sans-serif', fontWeight: 700 }}
                                    >
                                        {i + 1}
                                    </span>
                                    <div className="text-left">
                                        <div style={{ fontFamily: 'Inter, sans-serif', fontWeight: 600, fontSize: '0.82rem', color: isDark ? '#CBD5E1' : '#374151' }}>
                                            #{topic.tag}
                                        </div>
                                        <div style={{ fontSize: '0.72rem', color: isDark ? '#475569' : '#94A3B8' }}>
                                            {topic.posts.toLocaleString()} bài viết
                                        </div>
                                    </div>
                                </div>
                                <span
                                    className="text-xs px-2 py-0.5 rounded-full"
                                    style={{ background: 'rgba(34, 197, 94, 0.1)', color: '#22C55E', fontFamily: 'Inter, sans-serif', fontWeight: 600, fontSize: '0.7rem' }}
                                >
                                    {topic.trend}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Footer */}
            <div className="px-2 py-2">
                <div className="flex flex-wrap gap-x-3 gap-y-1">
                    {['Giới thiệu', 'Quyền riêng tư', 'Điều khoản', 'Trợ giúp'].map((link) => (
                        <button key={link} className="cursor-pointer" style={{ fontSize: '0.7rem', color: isDark ? '#334155' : '#CBD5E1', fontFamily: 'Inter, sans-serif' }}>
                            {link}
                        </button>
                    ))}
                </div>
                <div className="mt-2" style={{ fontSize: '0.68rem', color: isDark ? '#1E293B' : '#E2E8F0', fontFamily: 'Inter, sans-serif' }}>
                    © 2026 DTU Confession
                </div>
            </div>
        </div>
    );
}
