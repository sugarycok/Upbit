const express = require('express');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');
const socketIo = require('socket.io');
const bodyParser = require('body-parser');
const fs = require('fs');
const session = require('express-session');
const bcrypt = require('bcrypt');
const mysql = require('mysql');

const app = express();
const port = 3000;

// MySQL 연결 정보
const db = mysql.createConnection({
    host: '127.0.0.1',
    port: '3306',
    user: 'root',
    password: '0000',
    database: 'capstone'
});

// MySQL 연결
db.connect((err) => {
    if (err) {
        console.error('MySQL 연결 중 오류 발생:', err);
        process.exit(1); // 프로그램 종료
    }
    console.log('MySQL 데이터베이스에 연결되었습니다.');
});

// 세션 설정
app.use(session({
    secret: 'secret',
    resave: false,
    saveUninitialized: true
}));

// 정적 파일 제공
app.use(express.static(path.join(__dirname, 'public')));

// body-parser 설정
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// HTTP 서버 생성
const server = http.createServer(app);

// Socket.IO 서버 생성
const io = socketIo(server);

// 프로젝트 시작 시 api.txt 초기화 및 키 확인
fs.readFile('api.txt', 'utf8', (err, data) => {
    if (err) {
        console.error('api.txt 파일 읽기 중 오류 발생:', err);
        return;
    }

    const lines = data.split('\n');
    if (lines.length >= 4) {
        lines[0] = '';
        lines[1] = '';
        const updatedData = lines.join('\n');
        fs.writeFile('api.txt', updatedData, 'utf8', (err) => {
            if (err) {
                console.error('api.txt 파일 초기화 중 오류 발생:', err);
            } else {
                console.log('api.txt 파일이 초기화되었습니다.');
            }
        });
    } else {
        console.error('api.txt 파일 형식 오류');
    }

    // API 키 출력
    console.log(`업비트 API 키 확인 - Access Key: ${lines[0]}, Secret Key: ${lines[1]}`);
});

// 로그인 상태 확인 API
app.get('/getUsername', (req, res) => {
    if (req.session.username) {
        res.json({ username: req.session.username });
    } else {
        res.json({ username: null });
    }
});

// 회원가입 페이지
app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'register.html'));
});

// 회원가입 처리
app.post('/register', (req, res) => {
    const { name, username, password, phone, access_key, secret_key } = req.body;

    if (!name || !username || !password || !phone || !access_key || !secret_key) {
        return res.status(400).send('모든 필드를 입력해 주세요.');
    }

    // 사용자명(username) 중복 확인 쿼리
    const checkDuplicateQuery = `SELECT * FROM users WHERE username = ?`;
    db.query(checkDuplicateQuery, [username], async (checkErr, checkResult) => {
        if (checkErr) {
            console.error('사용자명 중복 확인 중 오류 발생:', checkErr);
            return res.status(500).send('회원가입 중 오류가 발생했습니다.');
        } else if (checkResult.length > 0) {
            // 사용자명이 이미 존재하는 경우
            return res.status(400).send('이미 존재하는 사용자명입니다.');
        } else {
            // 비밀번호 해시화
            const hashedPassword = await bcrypt.hash(password, 10);
            
            // 사용자명이 중복되지 않은 경우, 회원가입 정보를 데이터베이스에 저장하는 쿼리
            const insertQuery = `INSERT INTO users (name, username, password, phone, access_key, secret_key) VALUES (?, ?, ?, ?, ?, ?)`;
            db.query(insertQuery, [name, username, hashedPassword, phone, access_key, secret_key], (insertErr, insertResult) => {
                if (insertErr) {
                    console.error('회원가입 중 오류 발생:', insertErr);
                    return res.status(500).send('회원가입 중 오류가 발생했습니다.');
                } else {
                    console.log('회원가입이 성공적으로 완료되었습니다.');
                    res.redirect('/login');
                }
            });
        }
    });
});

// 로그인 페이지
app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

// 로그인 처리
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).send('아이디와 비밀번호를 입력해 주세요.');
    }

    // 사용자명(username)을 데이터베이스에서 확인하는 쿼리
    const loginQuery = `SELECT id, username, password, name, access_key, secret_key FROM users WHERE username = ?`;
    db.query(loginQuery, [username], async (err, result) => {
        if (err) {
            console.error('로그인 중 오류 발생:', err);
            return res.status(500).send('로그인 중 오류가 발생했습니다.');
        } else if (result.length === 0) {
            // 사용자명이 일치하지 않는 경우
            return res.status(401).send('사용자명 또는 비밀번호가 일치하지 않습니다.');
        } else {
            const user = result[0];
            const match = await bcrypt.compare(password, user.password);
            if (match) {
                // 로그인이 성공한 경우
                req.session.userId = user.id; // 세션에 사용자 ID 저장
                req.session.username = user.name; // 세션에 사용자 이름 저장
                req.session.access_key = user.access_key;
                req.session.secret_key = user.secret_key;

                // api.txt 파일 업데이트
                fs.readFile('api.txt', 'utf8', (err, data) => {
                    if (err) {
                        console.error('api.txt 파일 읽기 중 오류 발생:', err);
                        return res.status(500).send('api.txt 파일 읽기 중 오류 발생');
                    }

                    const lines = data.split('\n');
                    if (lines.length < 4) {
                        return res.status(500).send('api.txt 파일 형식 오류');
                    }

                    lines[0] = user.access_key;
                    lines[1] = user.secret_key;

                    const updatedData = lines.join('\n');
                    fs.writeFile('api.txt', updatedData, 'utf8', (err) => {
                        if (err) {
                            console.error('api.txt 파일 쓰기 중 오류 발생:', err);
                            return res.status(500).send('api.txt 파일 쓰기 중 오류 발생');
                        }

                        res.redirect('/');
                    });
                });
            } else {
                // 비밀번호가 일치하지 않는 경우
                res.status(401).send('사용자명 또는 비밀번호가 일치하지 않습니다.');
            }
        }
    });
});

// 로그아웃 처리
app.get('/logout', (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            console.error('로그아웃 중 오류 발생:', err);
            return res.status(500).json({ success: false, error: '로그아웃 중 오류가 발생했습니다.' });
        } else {
            // api.txt 파일 초기화
            fs.readFile('api.txt', 'utf8', (err, data) => {
                if (err) {
                    console.error('api.txt 파일 읽기 중 오류 발생:', err);
                    return res.status(500).json({ success: false, error: 'api.txt 파일 읽기 중 오류가 발생했습니다.' });
                }

                const lines = data.split('\n');
                if (lines.length >= 4) {
                    lines[0] = '';
                    lines[1] = '';
                    const updatedData = lines.join('\n');
                    fs.writeFile('api.txt', updatedData, 'utf8', (err) => {
                        if (err) {
                            console.error('api.txt 파일 초기화 중 오류 발생:', err);
                            return res.status(500).json({ success: false, error: 'api.txt 파일 초기화 중 오류가 발생했습니다.' });
                        } else {
                            res.json({ success: true });
                        }
                    });
                } else {
                    console.error('api.txt 파일 형식 오류');
                    res.status(500).json({ success: false, error: 'api.txt 파일 형식 오류' });
                }
            });
        }
    });
});

// API 엔드포인트: 코인 목록과 시세 가져오기
app.get('/api/coins', (req, res) => {
    const pythonProcess = spawn('python', ['list.py'], { encoding: 'utf-8' });

    let dataToSend = '';

    pythonProcess.stdout.on('data', (data) => {
        dataToSend += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            try {
                const result = JSON.parse(dataToSend);
                res.json(result);
            } catch (error) {
                console.error('JSON 파싱 중 오류 발생:', error);
                res.status(500).send('서버 오류');
            }
        } else {
            res.status(500).send('서버 오류');
        }
    });
});

// 자동 거래 시작
app.post('/start', (req, res) => {
    const { ticker, sid } = req.body;
    console.log('Received data - 티커:', ticker, '소켓 ID:', sid);
    const options = {
        hostname: 'localhost', // Flask 서버가 실행 중인 호스트
        port: 5002, // Flask 서버가 실행 중인 포트
        path: '/start',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const request = http.request(options, (response) => {
        let data = '';
        response.on('data', (chunk) => {
            data += chunk;
        });
        response.on('end', () => {
            console.log('Response from Flask server:', data);
            res.send(data);
        });
    });

    request.on('error', (e) => {
        console.error(`Problem with request: ${e.message}`);
        res.status(500).send('Error starting trading');
    });

    request.write(JSON.stringify({ ticker: ticker, sid: sid }));
    request.end();
});

// Socket.IO 연결 관리
io.of('/auto').on('connection', (socket) => {
    console.log('Client connected');

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });

    // 상태 업데이트 이벤트 처리
    socket.on('status_update', (data) => {
        io.of('/auto').emit('status_update', data);
    });
});

// 서버 시작
server.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
