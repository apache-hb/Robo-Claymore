import React from 'react';
import AnchorLink from 'react-anchor-link-smooth-scroll';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import './App.css';

export default function App() {
  return (
    <Router>
      <div>
        <div className="header">
          <a href="#" className="logo">Robo-Claymore</a>
          <div className="header-right">
            <AnchorLink href="#features">Features</AnchorLink>
            <AnchorLink href="#commands">Commands</AnchorLink>
            <AnchorLink href="#code">Code</AnchorLink>
            <Link to="/discord/login">Login</Link>
          </div>
        </div>

        <Route path="/discord/login" component={() => {
          window.location.href = "httplocalhost:8080/discord/login"
        }}/>
      </div>
    </Router>
  )
}
