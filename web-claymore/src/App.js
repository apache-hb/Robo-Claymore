import React, { Component } from 'react';
import './App.css';
import axios from 'axios';

class App extends Component {
  
  state = {
    redirect: null,
    name: null,
    id: null,
    dis: null,
    avatar: null
  }

  componentDidMount() {
    /*fetch("http://localhost:8000/info")
      .then(data => {
        console.log(data);
      })
      .catch(err => {
        console.log(err);
      });*/
      
    let req = new XMLHttpRequest();

    req.withCredentials = true;

    req.onreadystatechange = (e) => {
      if(req.readyState === 4) {
        console.log(e);
      }
    }

    req.onerror = (err) => {
      console.log(err);
    }

    req.open('GET', 'http://localhost:8000/info', true);
    req.send();

    
    /*axios.get('http://localhost:8000/info')
      .then(data => {
        let { name, id, dis, avatar } = data;
        this.setState({
          name: name,
          id: id,
          dis: dis,
          avatar: avatar
        });
        console.log(data);
      })
      .catch(err => {
        console.log(err);
      });*/
  }

  render() {
    let url = this.state.redirect;
    
    if(url !== null) {
      window.location.replace(url);
    }

    return (
      <div className="App">
        {/* enable fira mono font on the website */}
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tonsky/FiraCode@1.206/distr/fira_code.css"></link>
        <header className="App-header">
          {this.renderHeader()}
        </header>
        <div className="App-body">
          {this.renderBody()}
        </div>
      </div>
    );
  }

  renderBody() {
    return (
      <div>ajsdhakjsdh</div>
    );
  }

  renderHeader() {
    return (
      <div className="App-title-bar">
        <img 
          src={`${this.state.avatar}`}
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
      <button className="App-header-button" onClick={() => this.setState({ redirect: url })}>
        {name}
        <div className="App-header-button-popup"></div>
      </button>
    );
  }
}

export default App;
