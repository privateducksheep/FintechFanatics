import React from "react";
import { View, Text, Button } from "react-native";
import { useLocalSearchParams, router } from "expo-router";

export default function ReceiptScreen() {
  const params = useLocalSearchParams<{
    status?: string;
    to?: string;
    amount?: string;
    txHash?: string;
    error?: string;
  }>();

  const ok = params.status === "success";

  return (
    <View style={{ flex: 1, padding: 16, justifyContent: "center" }}>
      <Text style={{ fontSize: 22, marginBottom: 12 }}>
        {ok ? "✅ Payment Sent" : "❌ Payment Failed"}
      </Text>

      <Text style={{ marginBottom: 6 }}>To: {params.to}</Text>
      <Text style={{ marginBottom: 12 }}>Amount: {params.amount} XRP</Text>

      {ok ? (
        <Text selectable style={{ marginBottom: 12 }}>
          Tx Hash: {params.txHash || "(not returned)"}
        </Text>
      ) : (
        <Text selectable style={{ marginBottom: 12, color: "red" }}>
          Error: {params.error || "(unknown)"}
        </Text>
      )}

      <Button title="Back to Wallet" onPress={() => router.push("/wallet")} />
    </View>
  );
}
