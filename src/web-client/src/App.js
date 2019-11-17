import React, { useEffect, useReducer } from 'react';
import axios from 'axios';

import './App.css';

const reducer = (state, { type, message, ...rest }) => {
  const messages = state.slice();
  switch (type) {
    case 'ping':
      messages.push({ type, message: 'Heartbeat received' });
      return messages;
    case 'progress':
      const existing = messages.filter(
        m => 'progress' === m.type && m.job_id === rest.job_id,
      );
      if (existing.length === 1) {
        Object.assign(existing[0], { type, message, ...rest });
      } else {
        messages.push({ type, message, ...rest });
      }
      return messages;
    case 'info':
      messages.push({ type, message });
      return messages;
    default:
      throw new Error();
  }
};

const startJob = () => axios.get('/start/').then(console.log('Job started!'));

const App = () => {
  const [messages, dispatch] = useReducer(reducer, []);
  useEffect(() => {
    const socket = new WebSocket(
      'ws://' + window.location.host + '/ws/status/',
    );

    socket.onmessage = e => {
      const data = JSON.parse(e.data);
      const { message, type, ...rest } = data;
      if ('ping' === type) {
        socket.send(JSON.stringify({ type: 'ping' }));
      }
      dispatch({ type: type ? type : 'info', message, ...rest });
      console.info('Message received', message);
    };

    socket.onclose = e => {
      console.error('Chat socket closed unexpectedly');
    };
  }, []);
  return (
    <div className="App">
      <header className="App-header">
        <img src="http://mirskytech.com/wp-content/uploads/2014/05/pony.png" />
        <h1>Django Channels Demo</h1>
        <button onClick={startJob}>Start Expensive Job!</button>
      </header>
      {messages.map(message => (
        <Message message={message} />
      ))}
    </div>
  );
};

const COLORS = {
  info: 'green',
  warning: 'yellow',
  error: 'red',
  ping: 'lightred',
  progress: 'magenta',
};

const Message = ({ message: { type, message, ...rest } }) => (
  <div style={{ background: COLORS[type] }}>
    {message}
    {type === 'progress' && <progress max="100" value={rest.progress} />}
  </div>
);

export default App;
