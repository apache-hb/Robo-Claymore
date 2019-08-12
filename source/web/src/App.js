import React from 'react';
import AnchorLink from 'react-anchor-link-smooth-scroll';
import './App.css';

export default function App() {
  return (
    <div>
      <div className="header">
        <a href="#" className="logo">Robo-Claymore</a>
        <div className="header-right">
          <AnchorLink href="#features">Features</AnchorLink>
          <AnchorLink href="#commands">Commands</AnchorLink>
          <AnchorLink href="#code">Code</AnchorLink>
          <AnchorLink href="#login">Login</AnchorLink>
        </div>
      </div>
      <div className="content">
        <div className="top-section">
          <div className="top-header">
            <div className="top-title">
              <a className="invite-button" target="_blank" href="https://discordapp.com/oauth2/authorize?client_id=447920998621249536&amp;scope=bot&amp;permissions=66321471">Invite Claymore</a>
            </div>
          </div>
        </div>

        <div className="section">
          <a id="features"/>
          Features
          <ul>
            <li>Autorole</li>
            <li>Tags &amp; quotes</li>
            <li>Moderation</li>
            <li>Music player</li>
            <li>Custom commands</li>
          </ul>
        </div>

        <div className="section">
          <a id="commands"/>
          Commands
          <ul>
            <li></li>
          </ul>
        </div>

        <div className="section">
          <a id="code"/>
          Github
          <a className="invite-button" target="_blank" href="https://github.com/Apache-HB/Robo-Claymore">Source code</a>
        </div>

        <div className="section">
          <a id="login"/>
          Login
        </div>
      </div>
    </div>
  )
}
