import React, { useEffect, useState } from "react";
import axios from "axios";

import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Card,
  CardContent,
  Link,
  CircularProgress,
  TextField,
  Container,
  Box
} from "@mui/material";

import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

// MUI X Date Picker
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

import dayjs from "dayjs";


function App() {
  const [selectedDate, setSelectedDate] = useState(dayjs()); // 오늘 날짜
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);

  const formattedDate = selectedDate.format("YYYY-MM-DD");

  // 날짜 변경 또는 초기 로딩 시 fetch
  useEffect(() => {
    fetchNews(formattedDate);
  }, [formattedDate]);

  const fetchNews = async (date) => {
    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:8000/news?date=${date}`);
      setData(res.data);
    } catch (err) {
      console.error(err);
      setData({});
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="md" style={{ paddingTop: 32, paddingBottom: 32 }}>
      <Typography variant="h4" gutterBottom>
        쿠팡 뉴스 브라우저
      </Typography>

      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        선택한 날짜에 해당하는 뉴스를 토픽별로 분류하여 보여줍니다.
      </Typography>

      {/* 날짜 선택 UI */}
      <Box mb={3}>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DatePicker
            label="날짜 선택"
            value={selectedDate}
            onChange={(newValue) => setSelectedDate(newValue)}
            renderInput={(params) => <TextField fullWidth {...params} />}
          />
        </LocalizationProvider>
      </Box>

      {loading ? (
        <Box mt={5} display="flex" justifyContent="center">
          <CircularProgress />
        </Box>
      ) : (
        <div>
          {Object.keys(data).length === 0 && (
            <Typography color="text.secondary" style={{ marginTop: 16 }}>
              선택한 날짜의 뉴스가 없습니다.
            </Typography>
          )}

          {Object.keys(data).map((topic) => (
            <Accordion key={topic}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">{topic}</Typography>
              </AccordionSummary>
              <AccordionDetails>
                {data[topic].map((item) => (
                  <Card key={item.id} style={{ marginBottom: 16 }}>
                    <CardContent>
                      <Typography variant="h6">{item.title}</Typography>

                      <Typography
                        variant="body2"
                        color="text.secondary"
                        style={{ marginBottom: 8 }}
                      >
                        {new Date(item.pub_date).toLocaleString()}
                      </Typography>

                      <Typography variant="body1" style={{ marginBottom: 8 }}>
                        {item.description}
                      </Typography>

                      <Link href={item.link} target="_blank" underline="hover">
                        원문 보기 →
                      </Link>
                    </CardContent>
                  </Card>
                ))}
              </AccordionDetails>
            </Accordion>
          ))}
        </div>
      )}
    </Container>
  );
}

export default App;
