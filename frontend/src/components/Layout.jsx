import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { RightPanel } from './RightPanel';
import { useTheme } from '../context/ThemeContext';

export function Layout() {
    const { isDark } = useTheme();

    return (
        <div
            className="min-h-screen"
            style={{
                background: isDark ? '#0F0F13' : '#F0F2F8',
                fontFamily: 'Inter, sans-serif',
                transition: 'background 0.3s ease',
            }}
        >
            <Sidebar />

            <div className="lg:ml-64 flex justify-center">
                <div className="w-full max-w-5xl xl:max-w-6xl flex gap-4 px-4 py-6 xl:px-6">
                    <main className="flex-1 min-w-0 max-w-2xl pb-24 lg:pb-6">
                        <Outlet />
                    </main>

                    <aside className="hidden xl:block w-80 flex-shrink-0">
                        <div className="sticky top-6">
                            <RightPanel />
                        </div>
                    </aside>
                </div>
            </div>
        </div>
    );
}
