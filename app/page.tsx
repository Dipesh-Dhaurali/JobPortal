export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Welcome to Job Portal
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Find your perfect job or hire the right candidate
          </p>
          <div className="flex gap-4 justify-center">
            <button className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition">
              Browse Jobs
            </button>
            <button className="border border-blue-600 text-blue-600 px-8 py-3 rounded-lg hover:bg-blue-50 transition">
              Post a Job
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
          <div className="bg-white p-8 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-4">For Candidates</h3>
            <p className="text-gray-600">
              Discover thousands of job opportunities and advance your career
            </p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-4">For Employers</h3>
            <p className="text-gray-600">
              Find and hire the best talent for your organization
            </p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-4">Easy to Use</h3>
            <p className="text-gray-600">
              Simple and intuitive interface for seamless experience
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
