import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

// import logo from './logo.svg';
import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';
import { HelmetProvider } from 'react-helmet-async';


class App extends Component {
  render() {
    return (
    <div className="App">
      <HelmetProvider>
        <Header path />
        <Router>
          <Switch>
            <Route path="/" exact component={QuestionView} />
            <Route path="/add" component={FormView} />
            <Route path="/play" component={QuizView} />
            <Route component={QuestionView} />
          </Switch>
        </Router>
      </HelmetProvider>

    </div>
  );

  }
}

export default App;
