import { FunctionComponent } from "react";
import { Pressable, StyleSheet } from "react-native";
import Text from "./Text";

interface ChipProps {
  label: string;
  onPress: () => void;
  prefix?: JSX.Element;
  outline?: boolean;
}

const Chip: FunctionComponent<ChipProps> = ({ label, onPress, prefix, outline = false }) => {
  const styles = createStyles(outline);
  return (
    <Pressable style={styles.container} onPress={onPress}>
      {prefix}
      <Text tag='body' style={styles.label}>{label}</Text>
    </Pressable>
  );
};

const createStyles = (outline: boolean) => StyleSheet.create({
  container: {
    backgroundColor: outline ? undefined : COLORS.primary800,
    padding: 8,
    borderRadius: 16,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    borderColor: outline ? COLORS.primary800 : undefined,
    borderWidth: outline ? 3 : undefined,
  },
  label: {
    color: outline ? COLORS.primary800 : COLORS.neutral0
  }
});

export default Chip;