def split_socket_str(socket_str: str) -> list[str]:
    """Split str formatted socket into its parts: node, type, key."""
    return socket_str.split(".", 2)


def get_socket_str(node: str, type: str, key: str) -> str:
    return ".".join((node, type, key))
