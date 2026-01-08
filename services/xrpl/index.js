import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

app.get("/health", (req, res) => res.json({ ok: true, service: "xrpl" }));

app.listen(3001, () => console.log("XRPL service listening on http://localhost:3001"));
