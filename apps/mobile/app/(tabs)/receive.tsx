import React from "react";
import { View, Text } from "react-native";
import QRCode from "react-native-qrcode-svg";

export default function ReceiveScreen() {
  const address = "rPLACEHOLDER"; // temporary demo address

  const payload = JSON.stringify({ address });

  return (
    <View
      style={{
        flex: 1,
        padding: 16,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text style={{ fontSize: 20, marginBottom: 16 }}>Receive</Text>

      <QRCode value={payload} size={220} />

      <Text style={{ marginTop: 16 }} selectable>
        {address}
      </Text>

      <Text style={{ marginTop: 8, color: "#666" }}>
        QR contains {"{ address }"}
      </Text>
    </View>
  );
}
