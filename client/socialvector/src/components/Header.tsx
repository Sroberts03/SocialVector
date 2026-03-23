import logo from '../assets/logo.png';

export default function Header() {
    return (
        <header className="bg-gray-800 text-white py-4">
            <div className="container mx-auto flex items-center justify-between">
                <img src={logo} alt="SocialVector Logo" className="h-10 w-10" />
                <h1 className="text-2xl font-bold">SocialVector</h1>
                <nav>
                    <ul className="flex space-x-4">
                        <li><a href="#" className="hover:text-gray-400">Home</a></li>
                        <li><a href="#" className="hover:text-gray-400">Profile</a></li>
                        <li><a href="#" className="hover:text-gray-400">Messages</a></li>
                        <li><a href="#" className="hover:text-gray-400">Settings</a></li>
                    </ul>
                </nav>
            </div>
        </header>
    );
}