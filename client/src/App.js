import React from 'react';
import Home from './pages/Home';
import Navbar from './components/Navbar';

function App() {
  return (
    <div className="min-h-screen bg-background font-sans text-textMain selection:bg-accent1 selection:text-white">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <Home />
      </main>
    </div>
  );
}

export default App;
