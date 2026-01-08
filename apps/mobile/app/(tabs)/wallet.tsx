import React, { useEffect, useState } from "react";
import { View, Text, Button, ActivityIndicator } from "react-native";
import { apiGet, apiPost } from "../../src/api";
import { router } from "expo-router";


function shortAddr(addr?: string) {
  if (!addr) return "";
  return addr.length > 12 ? `${addr.slice(0, 6)}...${addr.slice(-6)}` : addr;
}

export default function WalletScreen() {
  const [address, setAddress] = useState<string>("");
  const [balance, setBalance] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");

  // TODO later: replace with real Firebase token
  const token: string | undefined = undefined;

  async function load() {
    setLoading(true);
    setError("");
    try {
      const init = await apiPost("/wallet/init", {}, token);
      setAddress(init.address);
      const bal = await apiGet("/wallet/balance", token);
      setBalance(bal.balance_xrp);
    } catch (e: any) {
      setError(e.message || String(e));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <View style={{ flex: 1, padding: 16, justifyContent: "center" }}>
      <Text style={{ fontSize: 22, marginBottom: 16 }}>Wallet</Text>

      {loading ? <ActivityIndicator /> : null}

      {!loading ? (
        <>
          <Text style={{ marginBottom: 8 }}>
            Address: <Text selectable>{shortAddr(address)}</Text>
          </Text>
          <Text style={{ marginBottom: 16 }}>
            Balance: <Text style={{ fontWeight: "bold" }}>{balance || "-"}</Text> XRP
          </Text>

          {error ? (
            <Text style={{ color: "red", marginBottom: 12 }} selectable>
              {error}
            </Text>
          ) : null}

          <Button title="Refresh" onPress={load} />
          <View style={{ height: 12 }} />
          <Button title="Receive (QR)" onPress={() => router.push("/receive")} />
          <View style={{ height: 12 }} />
          <Button title="Pay (Scan QR)" onPress={() => router.push("/pay")} />
        </>
      ) : null}
    </View>
  );
}
