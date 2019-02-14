import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import './App.css';

export default class App extends Component {
  
  headerHeight = 64;

  render() {
    return (
      <div className="App">
        {/* enable fira mono font on the website */}
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tonsky/FiraCode@1.206/distr/fira_code.css"></link>
        <header className="App-header">
          {this.renderHeader()}
        </header>
      </div>
    );
  }

  renderHeader() {
    return (
      <div className="App-title-bar">
        <img 
          src="https://cdn.discordapp.com/avatars/468828594202869771/42e46c1a23386cd099d784a57fe036ef.webp" 
          alt="Profile"
          align="left"
          className="App-title-image">
        </img>
        {this.renderHeaderButton("Discord", "https://discord.gg/y3uSzCK")}
        {this.renderHeaderButton("Github", "https://github.com/Apache-HB/Robo-Claymore")}
        {this.renderHeaderButton("Invite", "https://discordapp.com/oauth2/authorize?client_id=468828594202869771&scope=bot&permissions=8")}
      </div>
    );
  }

  renderHeaderButton(name, url) {
    return (
      <button className="App-header-button" onClick={this.redirect(url)}>
        {name}
        <div className="App-header-button-popup"></div>
      </button>
    );
  }

  redirect(url) {
    return <Redirect to={url}/>
  }
}
