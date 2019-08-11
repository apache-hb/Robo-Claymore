import React from 'react';
import AnchorLink from 'react-anchor-link-smooth-scroll';
import './App.css';

export default function App() {
  return (
    <div>
      <div className="header">
        <a href="#top" className="logo">Robo-Claymore</a>
        <div className="header-right">
          <AnchorLink href="#features">Features</AnchorLink>
          <AnchorLink href="#commands">Commands</AnchorLink>
          <AnchorLink href="#code">Code</AnchorLink>
          <AnchorLink href="#login">Login</AnchorLink>
        </div>
      </div>
      <div className="content">
        <a id="top" className="thing">Top</a>
        <a id="features" className="thing">Features</a>
        <a id="commands" className="thing">Commands</a>
        <a id="code" className="thing">Code</a>
        <a id="login" className="thing">Login</a>
      </div>
    </div>
  )
}
