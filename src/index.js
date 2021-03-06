// Import modules
const express = require('express');
const morgan = require('morgan');
const path = require('path');
const cors = require('cors');

global.processManager = require(path.join(__dirname, './lib/processManager.js'));

// Global variables
var app = express();


// Settings
app.set('trust proxy', true);
app.set('port', process.env.PORT || 8080);
global.processManager.MAX_PROCESS = 2;  

// Middlewares
app.use(cors());
// app.use(morgan('combined'));
app.use(express.json());

// Routes
app.use(require(path.join(__dirname, "routes/index.js")));
app.use(require(path.join(__dirname, "routes/execute.js")));
app.use(require(path.join(__dirname, "routes/apiExecute.js")));
app.use(require(path.join(__dirname, "routes/apiCompounds.js")));

// Static files
app.use(express.static(path.join(__dirname, 'public')));

// Start listening
app.listen(app.get('port'), () => {
    console.log('TurboPutative web application listening on port', app.get('port'));
})