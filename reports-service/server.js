const express = require('express');
const cors = require('cors');
const app = express();
const reportsRouter = require('./routes/reports');

app.use(cors());
app.use(express.json());
app.use('/api/reports', reportsRouter);

const PORT = process.env.PORT || 8083;
app.listen(PORT, () => {
  console.log(`Reports service running on port ${PORT}`);
});
