const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const PORT = process.env.PORT || 3000;
const http = require('http');
const server = http.createServer(app);
const io = require('socket.io')(server);
const path = require('path');

childPath = __dirname.split(path.sep);
childPath.pop();
childPath = childPath.join(path.sep);

const startDetectingScript = (socket) => {
  var spawn = require('child_process').spawn;
  var child = spawn('python3', ['.\\detectFace.py'], {
    cwd: childPath,
  });

  child.on('error', (error) => {
    console.error(error);
  });

  child.stdout.on('data', (data) => {
    console.log(data.toString());
    if (data.toString().includes('faceUUID')) {
      console.log(' ');
      child.kill('SIGINT');
      let uuid = data.toString().split(' ').pop().trim();
      console.log('|' + uuid + '|');
      console.log(' ');
      // loadPersonData(uuid);
      detectionFinished(socket, uuid);
    }
  });
};

const startDetectLoop = async (socket) => {
  // start python detect loop here
  console.log('Starting to detect');
  startDetectingScript(socket);
};

const detectionFinished = async (socket, uuid) => {
  console.log('Detection finished');
  profileData = await loadPersonData(uuid); // Replace with uuid variable
  io.emit('profileData', JSON.stringify(profileData).replaceAll('\\n', '|'));
};

const printProfileData = (socket, jsonStringData) => {
  console.log('Printing started');
  // start python printing script
  var spawn = require('child_process').spawn;
  var child = spawn(
    'python3',
    ['.\\print.py', JSON.parse(jsonStringData).uuid],
    {
      cwd: childPath,
    }
  );
  child.on('error', (error) => {
    console.error(error);
  });
  child.on('exit', () => {
    console.log('Printing Finished');
    socket.emit('thankyou');
  });
  // Once done, show thank you page
  // setTimeout(() => {
  //   console.log('Printing finished');
  //   socket.emit('thankyou');
  // }, 5000);
};

io.on('connection', (socket) => {
  console.log('User connected');

  socket.on('start', () => {
    startDetectLoop(socket);
  });

  socket.on('print', (jsonStringData) => {
    printProfileData(socket, jsonStringData);
  });

  // socket.emit('thankyou');

  socket.on('disconnect', () => {
    console.log('User disconnected');
  });
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const fs = require('fs');

const loadPersonData = async (uuid) => {
  let data = fs.readFileSync('../database/json_db.json', { encoding: 'utf8' });
  let result = JSON.parse(data).find((x) => x.uuid === uuid);
  // console.log(result);
  return result;
};

app.use('/', express.static(__dirname + '/public'));

server.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});

// TODO
// Add socket.io
// Start faceReq on demand
// Print information
