from typing import List, Tuple

from digitalocean import Image, Region, Size, SSHKey, Tag


def prepare_image_type_choices() -> List[Tuple[str, str]]:
    """
    Returns image type choices for the prompt.
    :return: list of 2-len tuples
    """
    return [
        ("Distribution only", "distribution"),
        ("Application only", "application"),
        ("All available images", "all"),
    ]


def prepare_image_choices(images: List[Image]) -> List[Tuple[str, Image]]:
    """
    Returns image choices for the prompt.
    :param list images: list of digitalocean.Image.Image instances
    :return: list of 2-len tuples
    """
    filtered_images = filter(lambda x: x.slug is not None, images)
    sorted_images = sorted(filtered_images, key=lambda x: x.slug, reverse=True)
    return [
        (f"{image.name} ({image.distribution})", image)
        for image in sorted_images
        if image.public and image.type == "snapshot"
    ]


def prepare_region_choices(regions: List[Region]) -> List[Tuple[str, Region]]:
    """
    Returns region choices for the prompt.
    :param list regions: list of digitalocean.Region.Region instances
    :return: list of 2-len tuples
    """
    regions_sorted = sorted(regions, key=lambda r: r.slug)
    return [(f"{region.name}", region) for region in regions_sorted]


def prepare_size_choices(sizes: List[Size]) -> List[Tuple[str, Size]]:
    """
    Returns size choices for the prompt.
    :param list sizes: list of digitalocean.Size.Size instances
    :return: list of 2-len tuples
    """
    sizes_sorted = sorted(sizes, key=lambda s: s.price_monthly)
    return [
        (
            f"{size.slug:15} | {'€' + str(size.price_monthly) + '/mo':10} | {'CPUs: ' + str(size.vcpus):^10}",
            size,
        )
        for size in sizes_sorted
    ]


def prepare_ssh_keys_addition_method_choices() -> List[Tuple[str, str]]:
    """
    Returns ssh addition method choices for the prompt.
    :return: list of 2-len tuples
    """
    remote = "Load ssh keys from your DO account (you'll be asked which " \
             "one(s) to use on next step)"
    local = "Load ssh public key from your local filesystem"
    return [(remote, "remote"), (local, "local")]


def prepare_ssh_key_choices(
    ssh_keys: List[SSHKey]
) -> List[Tuple[str, SSHKey]]:
    """
    Returns ssh key choices for the prompt.
    :param list ssh_keys: list of digitalocean.SSHKey.SSHKey instances
    :return: list of 2-len tuples
    """
    return [(f"{key.name}: {key.fingerprint}", key) for key in ssh_keys]


def prepare_tag_addition_method_choices() -> List[Tuple[str, str]]:
    """
    Returns tag addition method choices for the prompt.
    :return: list of 2-len tuples
    """
    return [
        ("Add remote (existing) tags only", "remote"),
        ("Add new tags only", "new"),
        ("Both remote and new tags", "both"),
    ]


def prepare_remote_tag_choices(tags: List[Tag]) -> List[Tuple[str, Tag]]:
    """
    Returns tag choices for the prompt.
    :param list tags: list of digitalocean.Tag.Tag instances
    :return: list of 2-len tuples
    """
    return [(tag.name, tag) for tag in tags]
