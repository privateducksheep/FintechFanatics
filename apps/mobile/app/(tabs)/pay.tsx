import React, { useEffect, useState } from "react";
import { View, Text, TextInput, Button, Alert } from "react-native";
import { CameraView, useCameraPermissions } from "expo-camera";
import { router } from "expo-router";
import { apiPost } from "../../src/api";

export default function PayScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const [scanned, setScanned] = useState(false);
  const [toAddress, setToAddress] = useState<string>("");
  const [amount, setAmount] = useState<string>("");

  // TODO later: replace with real login token
  const token: string | undefined = undefined;

  useEffect(() => {
    if (!permission) requestPermission();
  }, [permission]);

  function parseQR(data: string): string {
    try {
      const obj = JSON.parse(data);
      if (obj?.address && typeof obj.address === "string") return obj.address;
    } catch {}
    return data.trim();
  }

  async function sendPayment() {
    if (!toAddress) return Alert.alert("Scan a QR first");
    const n = Number(amount);
    if (!amount || Number.isNaN(n) || n <= 0) return Alert.alert("Invalid amount");

    try {
      const res = await apiPost(
        "/tx/send",
        { to_address: toAddress, amount_xrp: n },
        token
      );

      router.push({
        pathname: "/receipt",
        params: { status: "success", to: toAddress, amount: String(n), txHash: res?.tx_hash ?? "" },
      });
    } catch (e: any) {
      router.push({
        pathname: "/receipt",
        params: { status: "fail", to: toAddress, amount: String(n), error: e?.message ?? String(e) },
      });
    }
  }

  if (!permission) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <Text>Requesting camera permission...</Text>
      </View>
    );
  }

  if (!permission.granted) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center", padding: 16 }}>
        <Text style={{ marginBottom: 12 }}>Camera permission denied.</Text>
        <Button title="Grant Permission" onPress={requestPermission} />
      </View>
    );
  }

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <Text style={{ fontSize: 20, marginBottom: 12 }}>Pay (Scan QR)</Text>

      {!toAddress ? (
        <View style={{ flex: 1 }}>
          <View style={{ flex: 1, borderRadius: 12, overflow: "hidden" }}>
            <CameraView
              style={{ flex: 1 }}
              barcodeScannerSettings={{ barcodeTypes: ["qr"] }}
              onBarcodeScanned={
                scanned
                  ? undefined
                  : ({ data }) => {
                      const addr = parseQR(data);
                      setToAddress(addr);
                      setScanned(true);
                    }
              }
            />
          </View>

          <View style={{ height: 12 }} />
          <Button title="Scan Again" onPress={() => setScanned(false)} />
        </View>
      ) : (
        <View style={{ flex: 1 }}>
          <Text style={{ marginBottom: 8 }}>To:</Text>
          <Text selectable style={{ marginBottom: 16, fontWeight: "600" }}>
            {toAddress}
          </Text>

          <Text style={{ marginBottom: 8 }}>Amount (XRP)</Text>
          <TextInput
            value={amount}
            onChangeText={setAmount}
            keyboardType="decimal-pad"
            placeholder="e.g. 1.5"
            style={{ borderWidth: 1, borderColor: "#ccc", borderRadius: 10, padding: 12, marginBottom: 16 }}
          />

          <Button title="Send Payment" onPress={sendPayment} />
          <View style={{ height: 12 }} />
          <Button
            title="Change receiver"
            onPress={() => {
              setToAddress("");
              setScanned(false);
            }}
          />
        </View>
      )}
    </View>
  );
}
