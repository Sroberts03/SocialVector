import { Link } from 'react-router';
import logo from '../assets/logo.png';

const routes = () => {
    return [
        { name: 'Remy', path: '/create-event' },
        { name: 'Join', path: '/events' },
        { name: 'Settings', path: '/settings' }
    ]
}

export default function Header() {
    return (
        <header className="bg-white shadow-md">
            <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
                <div className="flex items-center space-x-3 min-w-[200px]">
                    <img src={logo} alt="SocialVector Logo" className="h-10 w-auto" />
                    <span className="text-xl font-semibold text-gray-800 tracking-tight">SocialVector</span>
                </div>
                <nav className="flex-1 flex justify-center">
                    <ul className="flex space-x-8">
                        {routes().map((route) => (
                            <li key={route.path}>
                                <Link to={route.path} className="text-gray-700 hover:text-blue-600 font-medium transition-colors duration-150">
                                    {route.name}
                                </Link>
                            </li>
                        ))}
                    </ul>
                </nav>
            </div>
        </header>
    );
}