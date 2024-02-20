#!/bin/bash

# Check if a filename was provided
if [ -z "$1" ]
then
  echo "Please provide a filename as an argument."
  exit 1
fi

fileName=$(basename "$1")
componentName="${fileName%.tsx}"


# Write 'hotdog' to the file
cat << EOF > "$1"
import { StyleSheet, View } from "react-native"
import { FunctionComponent } from "react"

interface ${componentName}Props {

}

const $componentName: FunctionComponent<${componentName}Props> = () => {
  return (
    <View>

    </View>
  )
}

const styles = StyleSheet.create({

})

export default $componentName
EOF
