export default function Home() {
    return (
        <div className="container mx-auto py-8">
            <h2 className="text-3xl font-bold mb-4">Welcome to SocialVector!</h2>
            <p className="text-gray-700 mb-6">
                Connect with friends, share your moments, and explore the world of social networking.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-4 rounded shadow">
                    <h3 className="text-xl font-semibold mb-2">Create Posts</h3>
                    <p className="text-gray-600">Share your thoughts and photos with your friends.</p>
                </div>
                <div className="bg-white p-4 rounded shadow">
                    <h3 className="text-xl font-semibold mb-2">Connect with Friends</h3>
                    <p className="text-gray-600">Find and connect with people you know.</p>
                </div>
                <div className="bg-white p-4 rounded shadow">
                    <h3 className="text-xl font-semibold mb-2">Explore Content</h3>
                    <p className="text-gray-600">Discover new content and trends from around the world.</p>
                </div>
            </div>
        </div>
    );
}